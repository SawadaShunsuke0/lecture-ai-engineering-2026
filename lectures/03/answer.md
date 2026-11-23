# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：第1回の素のLLMの回答は一般論でもっともらしい内容を答えているが、第3回のエージェントの回答は用語集の検索結果に基づいて答えている。
- `--trace` で見えたツール呼び出し（ツール名と引数）：
  - ツール名：search_glossaryを2回呼び出し
  - 引数：`LoRA`と`QLoRA`
- 1つの質問での LLM 呼び出し回数（`requests`）：2回
- 追加したツールと、docstring に書いた説明：
  - 追加したツール：make_quiz
  - docstringに書いた説明：
    - 指定した回の用語から1つを選び、確認問題と答えを返す。
    - 「第2回の確認問題を出して」のように、復習用の問題を求められたときに使う。

## 宿題

- 取り組んだレベル：基礎
- やったこと：`search_glossary` の docstring にある「用語を1つだけ入れる」という指示を「まとめて入れる」に変えた。
- 結果：
  - 引数の入れ方が変化し、呼び出し回数が減った。
    - 変更前：`search_glossary({'query': 'LoRA'})` と `search_glossary({'query': 'QLoRA'})` の2回（tool_calls=2）
    - 変更後：`search_glossary({'query': 'LoRA QLoRA'})` の1回（tool_calls=1）
  - 入力トークン数は減少したが、出力トークンが増加した。（回答の内容をまとめるような文章が最後に追加された。）
    | 項目 | 変更前 | 変更後 |
    |---|---|---|
    | input_tokens | 1374 | 1049（約24%減） |
    | output_tokens | 189 | 232（約23%増） |
- 気づき・疑問：
  - docstring を書き換えるだけでツールの使い方が変わることを確かめた。
  - LoRA の定義と QLoRA の定義が1つの結果として LLM に渡されたため、2つを比較してまとめるような回答が出力されたのだと考えられる。

- 取り組んだレベル：実装
- やったこと：
  - 学習記録を `learning_log/` に保存するツール `save_learning_log(content: str)` を `app/tools.py` に実装した。
  - `app/agent.py` では `requires_approval=True` を付けてツールを登録し、`output_type` は `[str, DeferredToolRequests]` とする。
  - CLI では、結果が `DeferredToolRequests` だったらツール名と引数（保存する内容）を表示し、「保存してよいですか？ [y/N]」と確認する。
  - 答えは `DeferredToolResults` にまとめ、それまでの会話履歴と一緒に渡して続きを実行する。y なら承認、それ以外は `ToolDenied` で拒否として扱う。
- 結果：
  - 「LoRAについて学習内容を保存して。」「QLoRAについて学習内容を保存して。」の2つを `--trace` 付きで実行した。
  - 確認に対して y と答えると `search_glossary` が実行され、`learning_log/` に日時入りのファイルがそれぞれ作成された。
  - 確認に対して N と答えると `search_glossary` は実行されず、`learning_log/` に新しいファイルは作成されなかった。
- 気づき・疑問：
  - `requires_approval=True` を付けるだけで、モデルがツールを呼ぼうとしてもすぐには実行されず、人の判断を待つようになることを確認した。
  - N と答えると「拒否された」という結果だけがモデルに渡されるため、エラーで止まることなくモデル自身がユーザーに分かる言葉で状況を説明できていた。
