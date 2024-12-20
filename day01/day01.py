import pandas as pd


def main():
    left = []
    right = []
    with open('input.txt') as f:
        for line in f:
            l, r = line.split()
            if len(l) > 0 and len(r) > 0:
                left.append(int(l))
                right.append(int(r))
    left.sort()
    right.sort()
    df = pd.DataFrame({'left': left, 'right': right})
    df['distance'] = abs(df['left'] - df['right'])
    print(df)
    distance = int(df['distance'].sum())

    score = 0
    for number in df.left:
        count = df['right'].value_counts().get(number, 0)
        score += int(count * number)
    print(f"{distance=} {score=}")

if __name__ == "__main__":
    main()
