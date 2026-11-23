"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 対話モードで続けて質問する（終了: exit）

ツールは持たないが、対話モードでは同じチャットセッションの会話履歴を保持する。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def create_chat():
    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)
    chat._aie_client = client
    return chat


def print_usage(response) -> None:
    usage = response.usage_metadata
    if usage is None:
        print("[tokens] 入力: 不明 / 出力: 不明")
        return

    input_tokens = usage.prompt_token_count
    output_tokens = usage.candidates_token_count
    print(
        f"[tokens] 入力: {input_tokens if input_tokens is not None else '不明'}"
        f" / 出力: {output_tokens if output_tokens is not None else '不明'}"
    )


def send_message(chat, question: str) -> str:
    response = chat.send_message(question)
    print_usage(response)
    return response.text


def ask(question: str) -> str:
    return send_message(create_chat(), question)


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?")
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        if args.question is not None:
            print(f"[質問] {args.question}\n")
            print(ask(args.question))
            return

        chat = create_chat()
        print("質問を入力してください（終了: exit / quit）")
        print(f"[質問] {DEFAULT_QUESTION}\n")
        print(send_message(chat, DEFAULT_QUESTION))

        while True:
            try:
                question = input("\n[質問] ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if question.lower() in {"exit", "quit"}:
                break
            if not question:
                continue
            print()
            print(send_message(chat, question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
