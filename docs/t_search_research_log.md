# t-search 研究作業ログ

## 2026-10-27 — 初回基準の確認とR5c

前回の研究実行ログはないため、今回の開始時点を比較基準として保存する。2026-10-26の設定時点に確認したR5b SHAと今回のheadは同じで、外部による追加更新はなかった。

| 対象 | 確認した状態 |
| --- | --- |
| main | `baed792419537c08d9bdc0990ed8b345549f6d98`。2026-09-11のPR #22統合。R4a〜R4dまで |
| 研究ブランチ | `research/record-stability-audit`、`a9c0849af737ca120833cb09eac369ef2de60fc4`。2026-09-11のR5b |
| 未マージ研究PR | [#23](https://github.com/kosukeya/t-search/pull/23)、Draft/open。R5a・R5bはmain未統合 |
| 差分 | mainに対して2コミット、8ファイル。R5a/b仕様・報告・実装・テスト・結果、README/roadmap |
| レビュー | submitted reviews・inline review threads・conversation commentsはいずれも0件 |
| 作業指示 | リポジトリの全treeと作業ディレクトリ上位を確認。AGENTS.mdなし |
| 読み取った研究根拠 | main/研究ブランチのREADME・roadmap、R5プロトコル・R5a監査・R5b報告/台帳、R4総括・台帳、R5b実装・テスト・保存結果とPR差分 |
| R5bのCI | head `a9c0849...`、[PR #34598342502](https://github.com/kosukeya/t-search/actions/runs/34598342502) / [push #34598339104](https://github.com/kosukeya/t-search/actions/runs/34598339104)ともsuccess。PRログはmerge ref `0002ef9`で1415テスト・18サブテスト成功 |
| mainのCI | head `baed792...` の[push #34595881776](https://github.com/kosukeya/t-search/actions/runs/34595881776)はsuccess |

### 開始時の要約

- **進捗:** R4統合済み、R5a/bはPR内で完了。R5c/dは未実施だった。
- **知見:** 記録の校正、固定測定の感度、操作クラス全体での古典化対照との差は別。全体表現と内部記録変化の両立は有限モデルの操作的な範囲で支持される。
- **未解決:** 最適読出しの具体的操作、E再アクセスで保証が失われる構成、Actuality/Potentialityとの解釈上の対応。
- **制約:** 既知状態対・固定基底・理想制御・単一コピー。Qの保証は以後E非結合。物理時計・単一結果・存在論的生成は未認定。
- **選択:** [R5c仕様](t_search_r5c_protocol.md)に従い「最大差の達成器とアクセス変更の反例」を一課題として実施する。

### 今回の実施と結果

[R5c報告・9件の主張台帳](t_search_r5c_access_guarantees.md)と[保存結果](../results/r5c_access_guarantees.json)を追加。35状態対でQ/Gの最適位相読出しを解析式と照合。初期Q差が零でもE逆結合後はQ差1/2となる反例を2件保存した。最大解析誤差3.33e-16、最大検証残差1.03e-15未満。既存R5bの25状態対を保存データと照合し、古い結果や来歴対象を保持した。

局所回帰は44テスト・18サブテスト成功。全リポジトリ回帰も起動した。初回の通常スレッド設定での実行は、数値計算の並列化を制限するため途中で中断し、同じソースを `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m pytest -q` で実行する。全体回帰の確定した実測結果、R5cコミット、新headのCIはPR #23のR5c検証欄に記録し、局所回帰や基点CIと区別する。新しい研究headをR5bのCI成功だけで検証済みとは扱わない。

README/roadmapのR4以前の本文はそのまま保持し、基点の684追跡ファイル中682ファイルは変更していない。変更は両進捗文書と新規6ファイル。R5b/R5cの来歴hash、相対リンク86件、文書の表の列数、`git diff --check`を確認した。

**次の判断:** R5dで操作依存の予測近似をActuality/Potentialityと全体履歴に対応付け、追加の存在論を仮定せず総括できる範囲を明確にする。R5dは未実施。

次回は、このログを含むコミット（Git履歴・PR #23から特定）とmain/研究ブランチの最新SHAを比較する。
