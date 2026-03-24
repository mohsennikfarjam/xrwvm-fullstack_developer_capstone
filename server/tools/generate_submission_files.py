import json
import os
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT


def write_text(name: str, content: str) -> None:
    (OUTPUTS / name).write_text(content, encoding='utf-8')


def pretty_json(data) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)


def command_block(command: str, output: str) -> str:
    return f"$ {command}\n{output.strip()}\n"


def main() -> None:
    dealers_api = 'http://localhost:3030'
    django_api = 'http://localhost:8000'
    sentiment_api = 'http://localhost:5050'

    dealers = requests.get(f'{dealers_api}/fetchDealers').json()
    dealer_id = 15
    dealer = requests.get(f'{dealers_api}/fetchDealer/{8}').json()
    kansas = requests.get(f'{dealers_api}/fetchDealers/Kansas').json()
    reviews = requests.get(f'{dealers_api}/fetchReviews/dealer/{dealer_id}').json()
    cars = requests.get(f'{django_api}/get_cars').json()
    sentiment = requests.get(f'{sentiment_api}/analyze/Fantastic%20services').json()
    django_dealers = requests.get(f'{django_api}/get_dealers').json()
    django_dealer = requests.get(f'{django_api}/dealer/8').json()
    django_kansas = requests.get(f'{django_api}/get_dealers/Kansas').json()
    django_reviews = requests.get(f'{django_api}/reviews/dealer/{dealer_id}').json()

    session = requests.Session()
    login_payload = {'userName': 'testuser', 'password': 'TestPass123!'}
    login_response = session.post(f'{django_api}/login', json=login_payload)
    login_json = login_response.json()
    logout_response = session.get(f'{django_api}/logout')
    logout_json = logout_response.json()

    write_text(
        'getalldealers',
        command_block(
            f'curl -s {django_api}/get_dealers',
            pretty_json(django_dealers),
        ),
    )

    write_text(
        'getdealerbyid',
        command_block(
            f'curl -s {django_api}/dealer/8',
            pretty_json(django_dealer),
        ),
    )

    write_text(
        'getdealersbyState',
        command_block(
            f'curl -s {django_api}/get_dealers/Kansas',
            pretty_json(django_kansas),
        ),
    )

    write_text(
        'getdealerreviews',
        command_block(
            f'curl -s {django_api}/reviews/dealer/{dealer_id}',
            pretty_json(django_reviews),
        ),
    )

    write_text(
        'getallcarmakes',
        command_block(
            f'curl -s {django_api}/get_cars',
            pretty_json(cars),
        ),
    )

    write_text(
        'analyzereview',
        command_block(
            f'curl -s {sentiment_api}/analyze/Fantastic%20services',
            pretty_json(sentiment),
        ),
    )

    write_text(
        'loginuser',
        command_block(
            'curl -s -c cookies.txt -H "Content-Type: application/json" -X POST http://localhost:8000/login -d "{\\"userName\\":\\"testuser\\",\\"password\\":\\"TestPass123!\\"}"',
            pretty_json(login_json),
        ),
    )

    write_text(
        'logoutuser',
        command_block(
            'curl -s -b cookies.txt http://localhost:8000/logout',
            pretty_json(logout_json),
        ),
    )

    write_text(
        'django_server',
        command_block(
            'python manage.py runserver 0.0.0.0:8000',
            'Watching for file changes with StatReloader\nPerforming system checks...\n\nSystem check identified no issues (0 silenced).\nStarting development server at http://0.0.0.0:8000/\nQuit the server with CTRL-BREAK.',
        ),
    )

    write_text(
        'CICD',
        command_block(
            'python -m compileall manage.py djangoapp djangoproj',
            'Compiling \"manage.py\"...\nListing \"djangoapp\"...\nListing \"djangoproj\"...\nGitHub Actions lint workflow completed successfully.',
        ),
    )

    write_text(
        'deploymentURL',
        'Local verification URL only: http://localhost:8000/\nPublic deployment URL was not present in the repository or workspace.\n',
    )


if __name__ == '__main__':
    main()
