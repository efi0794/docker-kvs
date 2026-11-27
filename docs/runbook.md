# 障害対応演習

1. `docker compose up -d` で起動し、`docker compose ps` を確認。
2. http://localhost:8080 と http://localhost:8081 を開き、正常時の応答を記録。
3. `docker compose stop web` で障害を再現し、15秒後に監視結果を確認。
4. `docker compose logs web` と `docker compose ps -a` で原因を調査。
5. `docker compose start web` で復旧し、監視結果を確認。
6. `docker compose exec redis redis-cli SET lab hello` を実行し、`docker compose restart redis` 後に `docker compose exec redis redis-cli GET lab` で永続化を確認。
7. `docker compose down` で終了（ボリュームは保持）。

## 実測記録（未実施）

| 項目 | 期待結果 | 実測 |
|---|---|---|
| 通常時 | HTTP 200 | 未実施 |
| 停止時 | ok=false | 未実施 |
| 復旧時 | ok=true | 未実施 |
| Redis再起動 | helloを保持 | 未実施 |

監視結果はメモリ上の直近120件のみ。履歴の永続化、認証、通知は今後の課題。
