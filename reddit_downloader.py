# Note: praw is limited to 1k posts. For more, use https://github.com/mattpodolak/pmaw

import argparse
import json
import os
import praw
from tqdm import tqdm


def create_client():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    if client_id is None:
        print("REDDIT_CLIENT_ID not set")
        return

    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    if client_secret is None:
        print("REDDIT_CLIENT_SECRET not set")
        return

    user_agent = os.getenv("REDDIT_USER_AGENT")
    if user_agent is None:
        print("REDDIT_USER_AGENT not set")
        return

    client = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
    return client


def get_author_id(x):
    if x.author is not None:
        try:
            return x.author.id
        except:
            return ""


def extract_comment_data(comment, include_author=False):
    comment_data = {
        "body": comment.body,
        "body_html": comment.body_html,
        "created_utc": comment.created_utc,
        "distinguished": comment.distinguished,
        "downs": comment.downs,
        "edited": comment.edited,
        "id": comment.id,
        "link_id": comment.link_id,
        "name": comment.name,
        "num_reports": comment.num_reports,
        "parent_id": comment.parent_id,
        "permalink": comment.permalink,
        "score": comment.score,
        "subreddit_id": comment.subreddit_id,
        "ups": comment.ups,
    }
    if include_author:
        comment_data["author"] = get_author_id(comment)
    return comment_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_path")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--overwrite", default=False, action="store_true")
    parser.add_argument("--include_author", default=False, action="store_true")
    parser.add_argument("--include_comments", default=False, action="store_true")
    parser.add_argument("--time_filter", default="all", choices=["all", "day", "hour", "month", "week", "year"])
    args = parser.parse_args()
    print(args)

    client = create_client()
    if client is None:
        print("failed to create reddit client")
        return

    if os.path.exists(args.output_path) and not args.overwrite:
        print("output_path already exists:", args.output_path)
        return

    subreddit = client.subreddit("formcheck")
    for _ in subreddit.top(limit=2):
        pass
    print("Warmup complete")

    with open(args.output_path, "w") as f:
        for post in tqdm(subreddit.top(limit=args.limit, time_filter=args.time_filter), total=(args.limit or float("inf"))):
            if post.is_video:
                post_data = {
                    "created_utc": post.created_utc,
                    "distinguished": post.distinguished,
                    "downs": post.downs,
                    "edited": post.edited,
                    "id": post.id,
                    "is_original_content": post.is_original_content,
                    "is_self": post.is_self,
                    "link_flair_text": post.link_flair_text,
                    "locked": post.locked,
                    "media": post.media,
                    "name": post.name,
                    "num_comments": post.num_comments,
                    "num_reports": post.num_reports,
                    "over_18": post.over_18,
                    "permalink": post.permalink,
                    "score": post.score,
                    "selftext": post.selftext,
                    "subreddit_id": post.subreddit_id,
                    "title": post.title,
                    "ups": post.ups,
                    "upvote_ratio": post.upvote_ratio,
                    "url": post.url,
                    "view_count": post.view_count,
                }

                if args.include_author:
                    post_data["author"] = get_author_id(post)

                if args.include_comments:
                    comments = []
                    for comment in post.comments.list():
                        comment_data = extract_comment_data(comment, include_author=args.include_author)
                        comments.append(comment_data)
                    post_data["comments"] = comments

                f.write(json.dumps(post_data) + "\n")









if __name__ == "__main__":
    main()
