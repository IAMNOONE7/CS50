import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    n = len(corpus)

    probs = {p: 0.0 for p in corpus.keys()}

    links = corpus[page]

    if len(links) == 0:
        links = set(corpus.keys())

    base = (1 - damping_factor) / n
    for p in probs:
        probs[p] = base

    share = damping_factor / len(links)
    for p in links:
        probs[p] += share

    return probs


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())

    counts = {p: 0 for p in pages}
    current = random.choice(pages)
    counts[current] += 1

    for _ in range (1,n):
        tm = transition_model(corpus, current, damping_factor)

        next_page = random.choices(population=list(tm.keys()), weights = list(tm.values()),k=1)[0]

        counts[next_page] += 1
        current = next_page

    ranks = {p: counts[p] / n for p in pages}

    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    n = len(pages)
    d = damping_factor

    adj = {}
    for p, links in corpus.items():
        adj[p] = links if len(links) > 0 else set(pages)

    pr = {p:1 / n for p in pages}

    while True:
        new_pr = {}

        for p in pages:
            x = 0.0
            for q in pages:
                if p in adj[q]:
                    x += pr[q]/len(adj[q])

            new_pr[p] = (1 - d) / n + d * x

        dt = [abs(new_pr[p] - pr[p]) for p in pages]
        pr = new_pr
        if max(dt) < 0.001:
            break

    return pr


if __name__ == "__main__":
    main()
