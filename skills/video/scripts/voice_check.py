#!/usr/bin/env python3
"""Transcribe a voice take and diff it against the script.

    python3 voice_check.py voice/SCRIPT-take1.mp3 SCRIPT.txt --lang fr

Engine: whisper.cpp (`whisper-cli` on PATH + a model file in --model or $WHISPER_CPP_MODEL),
else the `openai-whisper` Python package (--model is then a model name, default "turbo").
Tone tags, punctuation and case are ignored. Differences that are numbers (digits vs words) or rough
homophones are listed "to check"; real word changes are errors and the exit code is 1.
A clean check is not a listening: a human still has to listen to the take.
"""
import argparse, difflib, os, pathlib, re, shutil, subprocess, sys, tempfile, unicodedata

NUMBER_WORDS = set(("zéro un une deux trois quatre cinq six sept huit neuf dix onze douze treize quatorze quinze "
                    "seize vingt trente quarante cinquante soixante cent cents mille et zero one two three four five "
                    "six seven eight nine ten eleven twelve twenty thirty forty fifty sixty seventy eighty ninety "
                    "hundred thousand and").split())


def words(text):
    text = re.sub(r"\[[^\]]*\]", " ", text).lower().replace("’", "'").replace("-", " ")
    text = unicodedata.normalize("NFC", text)
    return [w for w in re.split(r"[^\w']+", text) if w.strip("'")]


def rough_key(w):
    # shortcut: crude French/English homophone folding (maire/mer, taxe/taxes); good enough to triage, not to judge
    w = "".join(c for c in unicodedata.normalize("NFD", w) if unicodedata.category(c) != "Mn")
    w = w.replace("aux", "au").replace("ai", "e").replace("ei", "e").replace("en", "an").replace("qu", "c")
    w = re.sub(r"(.)\1", r"\1", w)
    for _ in range(3):
        for suffix in ("ez", "er", "ee", "es", "e", "s", "x", "t", "z"):
            if w.endswith(suffix) and len(w) > len(suffix) + 1:
                w = w[: -len(suffix)]
                break
    return w


def is_soft(ref, hyp):
    # numbers are compared out (words in the script, digits in the transcript); what remains must match
    r = [x for x in ref.split() if x not in NUMBER_WORDS]
    h = [x for x in hyp.split() if not re.search(r"[0-9%€$£]", x)]
    return [rough_key(x) for x in r] == [rough_key(x) for x in h]


def compare(script, transcript):
    ref, hyp = words(script), words(transcript)
    sm = difflib.SequenceMatcher(a=ref, b=hyp, autojunk=False)
    diffs = [(" ".join(ref[i1:i2]), " ".join(hyp[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
    return sm.ratio(), [d for d in diffs if is_soft(*d)], [d for d in diffs if not is_soft(*d)]


def transcribe(audio, lang, model):
    if shutil.which("whisper-cli") and (model or os.environ.get("WHISPER_CPP_MODEL")):
        with tempfile.TemporaryDirectory() as tmp:
            wav = pathlib.Path(tmp) / "a.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(audio), "-ar", "16000", "-ac", "1", str(wav)], check=True)
            return subprocess.run(["whisper-cli", "-m", model or os.environ["WHISPER_CPP_MODEL"], "-l", lang, "-nt", "-np",
                                   "-f", str(wav)], capture_output=True, text=True, check=True).stdout
    try:
        import whisper
    except ImportError:
        sys.exit("No engine: install whisper.cpp (whisper-cli + model) or `pip install openai-whisper`.")
    return whisper.load_model(model or "turbo").transcribe(str(audio), language=lang)["text"]


def self_test():
    ratio, soft, hard = compare("[excited] Il l'a jeté, quinze mille euros.", "Il l'a acheté, 15 000 euros.")
    assert hard == [("jeté quinze mille", "acheté 15 000")], hard
    assert compare("Quinze mille euros.", "15 000 euros.")[1:] == ([("quinze mille", "15 000")], [])
    assert compare("La taxe du maire.", "La taxes du mer.")[2] == []
    print("self-test ok")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("audio", nargs="?", type=pathlib.Path)
    p.add_argument("script", nargs="?", type=pathlib.Path)
    p.add_argument("--lang", default="fr")
    p.add_argument("--model", default=None, help="whisper.cpp model path, or openai-whisper model name")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        return self_test()
    if not (a.audio and a.script):
        p.error("audio and script are required")
    transcript = transcribe(a.audio, a.lang, a.model)
    a.audio.with_name(a.audio.stem + "-transcript.txt").write_text(transcript)
    ratio, soft, hard = compare(a.script.read_text(encoding="utf-8"), transcript)
    print(f"{a.audio.name}: similarity {ratio:.3f}")
    if soft:
        print("  to check (numbers / homophones):", soft)
    if hard:
        print("  WORD DIFFERENCES:", hard)
    if not (soft or hard):
        print("  no difference")
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
