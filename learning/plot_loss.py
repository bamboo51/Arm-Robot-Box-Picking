"""Plot the ACT training loss from lerobot-train logs (several logs for a resumed run are merged by step).

uv run --with matplotlib python plot_loss.py                              # train.log + train_resume.log
uv run --with matplotlib python plot_loss.py run1.log run2.log -o loss.png
"""
import argparse
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

STEP = re.compile(r"\bstep:\s*([\d.]+)([KM]?)")
LOSS = re.compile(r"\bloss:\s*([\d.]+)")


def parse(line: str) -> tuple[float, float] | None:
    """(step, loss) from one log line like 'step:1K smpl:64K ... loss:0.123 ...', or None."""
    s, l = STEP.search(line), LOSS.search(line)
    if not (s and l):
        return None
    return float(s.group(1)) * {"": 1, "K": 1e3, "M": 1e6}[s.group(2)], float(l.group(1))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("logs", nargs="*", default=["train.log", "train_resume.log"])
    parser.add_argument("-o", "--out", default="loss.png")
    args = parser.parse_args()

    points = {}
    for path in args.logs:
        try:
            with open(path) as f:
                points.update(p for p in map(parse, f) if p)  # a resumed log overwrites repeated steps
        except FileNotFoundError:
            print(f"skip {path} (not found)")
    if not points:
        raise SystemExit("no 'step:... loss:...' lines found; check the log files")

    steps = sorted(points)
    loss = [points[s] for s in steps]
    plt.figure(figsize=(6, 3.5))
    plt.plot(steps, loss)
    plt.yscale("log")
    plt.xlabel("training step")
    plt.ylabel("training loss (log scale)")
    plt.title("ACT training loss")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(args.out, dpi=150)
    print(f"{len(steps)} points, step {steps[0]:.0f} -> {steps[-1]:.0f}, loss {loss[0]:.3f} -> {loss[-1]:.3f}; saved {args.out}")

if __name__ == "__main__":
    main()
