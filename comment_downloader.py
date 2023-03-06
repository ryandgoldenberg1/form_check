import argparse
import json
from tqdm import tqdm
from praw.models import MoreComments
import reddit_downloader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("output_path")
    parser.add_argument("--include_author", default=False, action="store_true")
    args = parser.parse_args()
    print(args)

    client = reddit_downloader.create_client()
    if client is None:
        print("failed to create reddit client")
        return

    with open(args.input_path) as f:
        metadata = [json.loads(l) for l in f.readlines()]
    print("read metadata rows:", len(metadata))

    with open(args.output_path, "w") as f:
        for row in tqdm(metadata):
            id = row["id"]
            submission = client.submission(id)
            # top-level only!
            comments = []
            for comment in submission.comments:
                if not isinstance(comment, MoreComments):
                    comment_data = reddit_downloader.extract_comment_data(comment, include_author=args.include_author)
                    comments.append(comment_data)
            output = {"id": id, "comments": comments}
            f.write(json.dumps(output) + "\n")


if __name__ == "__main__":
    main()
