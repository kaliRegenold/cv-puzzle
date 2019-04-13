import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Solve puzzles with computer vision.")
    parser.add_argument("--finished", "-c", help="Path to image of finished puzzle.")
    parser.add_argument("--scattered", "-s", help="Path to image of scattered puzzle.")
    parser.add_argument("--method", "-m", default="convolution", help="Method to solve puzzle.")

    return parser.parse_args()

def main(args):
    ...

if __name__ == "__main__":
    main(parse_args())
