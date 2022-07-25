import requests
from bs4 import BeautifulSoup

cached_so_url = 'https://bites-data.s3.us-east-2.amazonaws.com/so_python.html'


def top_python_questions(url=cached_so_url):
    """Use requests to retrieve the url / html,
       parse the questions out of the html with BeautifulSoup,
       filter them by >= 1m views ("..m views").
       Return a list of (question, num_votes) tuples ordered
       by num_votes descending (see tests for expected output).
    """
    response = requests.get(url)
    # if response.status_code == 200:
    #     print('Success!')
    # elif response.status_code == 404:
    #     print('Not Found.')
    soup = BeautifulSoup(response.content, 'html.parser')

    valid_questions = []
    # we must extract the parent 'question-summary', and from it, extract the title and views
    questions = soup.find_all("div", class_="question-summary")
    for q in questions:
        qtty = q.find("div", class_="views supernova")
        if qtty is None:
            qtty = q.find("div", class_="views hot")
        if qtty is None:
            qtty = q.find("div", class_="views warm")
        if qtty is None:
            assert 1 == 2, "No views found"
        # let's get the views, but soup.find gives "154,183 views" so we need to remove 'views' then the commas
        views = int(''.join(qtty["title"].split(" ")[0].split(",")))
        vote = int(q.find("span", class_="vote-count-post").text)
        question = q.find("a", class_="question-hyperlink").text.strip()
        # print(question, vote, views)
        if views > 1e6:
            valid_questions.append((question, vote))
    return sorted(valid_questions, key=lambda qv: qv[1], reverse=True)

if __name__ == "__main__":
    ans = top_python_questions(cached_so_url)
    print('\n'.join((str(xy) for xy in ans)))
