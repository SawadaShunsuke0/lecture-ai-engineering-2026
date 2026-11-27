# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：
  - fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
  - glossary_search_glossary({'query': 'Model Context Protocol'})
- STEP 4 の [tool call]：aws_aws___search_documentation({'search_phrase': 'Amazon S3 versioning overview', 'topics': ['general']})
- 気づき・疑問：STEP 3 では URL の要約だけを頼んでいたが、用語集のツールも呼び出されており、サーバーが増えるとモデルの判断で質問に必要なツール以外も呼び出されることがあると気づいた。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎
- やったこと：用語集のMCPサーバに `get_lecture_summary` ツールを公開した。
- 結果：「第2回では何を学びますか」という質問に対して、`glossary_get_lecture_summary({'lecture': 2})` とツールを呼び出してモデルは適切に回答していた。
- 気づき・疑問：「エージェント作成」と「ツール作成・公開」の作業を分けることができるというMCPサーバの利点を実際に確かめられた。

- 取り組んだレベル：実装
- やったこと：
  - 用語集のMCPサーバに `make_quiz` ツールを公開した。
  - 引数が範囲外のときのメッセージを改良した。
    - 講義自体が存在しない場合：講義が存在しないことと用意されている回を返す。
    - 講義は存在するが、用語が存在しない場合：講義が存在することと用語集に登録されていないことを返す。
- 結果：
  - 「第2回のクイズを作って」という質問に対して、`glossary_make_quiz({'lecture': 2})` とツールを呼び出してモデルは適切に回答していた。
  - 「第99回のクイズを作って」という質問に対して、`glossary_make_quiz({'lecture': 99})` とツールを呼び出し、`{"error": "第99回は存在しません。用意されている回: 第1回、第2回、第3回、第4回、第6回。"}` とわかりやすいメッセージを返してモデルは適切に回答していた。
- 気づき・疑問：ツールの返り値はモデルへ入力されるので、次の判断に必要な情報まで入れた方がよいのではないかと考えた。
