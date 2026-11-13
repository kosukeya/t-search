# 記録フィードバック下の正の分枝確率下限

2026-11-06。[実行前仕様](t_search_feedback_count_bound_protocol.md)の一課題を完了した。基点は [4e962b9](https://github.com/kosukeya/t-search/commit/4e962b9b42918b841e26775737e95cd62e7b5088)。記録フィードバックの三監査は [Draft PR #25](https://github.com/kosukeya/t-search/pull/25) の同一系列にあり、mainの [96aea72](https://github.com/kosukeya/t-search/commit/96aea72c205b130e5f6fc83e3abbc415bd5268ab) はR5dと時間平均までの六補足を統合済み。

旧KL下限が1.3553%の確率で失敗した固定1000試行の制御で、事前に倍率4を固定した下限は98.6311%の経路で正になり、失敗確率は0.3817%だった。同じ経路で前回の有効な加法下限は全てゼロ。今回の1%は全経路での失敗予算であり、正の下限が出た経路に限定すると失敗率が1%を超える条件もあった。

## 1. 問いと比較条件

**記録に依存して試行確率が変わるとき、有限な成功数から、経路に沿う予測可能平均へ正の下限を与えられるか。** [旧KLの被覆監査](t_search_kl_feedback_audit.md)で使った六条件の制御を保持し、下限の計算法だけを変えた。全体の試行数 $N$ と指数の底4を観測前に固定する。底4は簡単な整数判定を持つ候補として選んだ。倍率の比較最適化は保留する。

各二値スコア $X_t$ に対し、過去の全古典記録を $F_{t-1}$、$p_t=E[X_t\mid F_{t-1}]$ とする。処理の選択に使えるのは過去の記録であり、現在ブロックの測定結果は次の処理から反映する。対象は実現経路上の $\mu_N=\sum_{t=1}^N p_t/N$。量子ブロック共用、入力と環境のリセット、校正などは [前段の信頼条件](t_search_record_feedback.md) のまま、数値対照の校正予算はゼロ。

## 2. 固定倍率の下限

$S_t=\sum_{i=1}^t X_i$、$M_0=1$ とおく。条件付き二値分布から $E[4^{X_t}\mid F_{t-1}]=1+3p_t$。したがって

$$
M_t=\frac{4^{S_t}}{\prod_{i=1}^t(1+3p_i)}
$$

は非負マルチンゲールで、固定 $N$ において $E[M_N]=1$。算術・幾何平均の不等式を各経路で適用すると

$$
\prod_{t=1}^N(1+3p_t)\le (1+3\mu_N)^N,\qquad
M_N\ge \frac{4^{S_N}}{(1+3\mu_N)^N}.
$$

片側予算 $\beta=0.01$ として、観測した成功数だけで求まる下限を

$$
L_4(S_N,N)=\max\!\left(0,\frac{(4^{S_N}/100)^{1/N}-1}{3}\right)
$$

とする。$L_4>\mu_N$ なら $M_N>100$ なので、Markovの不等式により $P(L_4>\mu_N)\le0.01$。$L_4>0$ の条件は $4^{S_N}>100$、すなわち $S_N\ge4$。一般の予測可能な二値列についての被覆は、この解析から従う。有限の対照計算は下限の有用性を評価する。

一次資料では、指数過程を条件付きで正規化する構成を Howard, Ramdas, McAuliffe & Sekhon の *Time-uniform Chernoff bounds via nonnegative supermartingales* §2.1 の Definition 1 と直後のMGFによる構成で照合した。上の式はその一般的手法の固定倍率での適用で、経路ごとの積に算術・幾何平均を用いた。新規性は既知のマルチンゲール原理に置かず、旧KLが失敗した同じ模型での定量比較に置く。[著者論文](https://arxiv.org/pdf/1808.03204)

## 3. 事前固定した六条件

旧KL境界に初到達するか32成功で切り替えるまで、活動時の確率 $p=1/D$ を使う。以後の確率は0とし、残りも全て記録する。活動期間を $\tau$ とすれば $\mu_N=\tau/(DN)$。終端の $(\tau,s)$ での失敗は

$$
4^s(DN)^N > 100(DN+3\tau)^N
$$

と同値。各成功数に対する境界は $\tau$ について単調なので、二分探索と整数比較で厳密に決まる。以下は正確な整数分子からの表示丸め。

| N | 活動時p | 旧KLの失敗 | 倍率4の失敗 | 倍率4で下限が正 | 正の下限を出した経路内の失敗 |
| --- | --- | --- | --- | --- | --- |
| 100 | 1/1000 | 0.55828% | 0 | 0 | 条件事象の確率0 |
| 100 | 1/100 | 0.65250% | 0.05615% | 1.68867% | 3.32514% |
| 1000 | 1/1000 | 0.99231% | 0.06258% | 1.70794% | 3.66427% |
| 1000 | 1/100 | 1.35529% | 0.38174% | 98.63112% | 0.38704% |
| 10000 | 1/1000 | 1.74724% | 0.39602% | 98.23893% | 0.40312% |
| 10000 | 1/100 | 1.55734% | 0.37257% | 99.63827% | 0.37392% |

失敗なら必ず下限が正なので、右端は失敗確率を正の下限の確率で割った値。主例では加法下限がゼロだった経路の大半で正の値を得た。一方、最小期待カウントの条件では最大成功数が3で、全経路で下限がゼロ。別の二条件では正の下限は約1.7%の経路だけで、右端の確率は3%を超えた。**保証を発行した場合だけの誤り率に1%を使うことはできない。**

全六条件で終端の最大成功数の二乗が $2N$ 以下だった。$\log 100>4$ と合わせれば、前段の加法下限が全経路でゼロになることを整数条件で検算できる。倍率4による優位は条件依存で、構成カウント $N=100,S=50$ では倍率4が約0.30333、加法法が約0.34826。倍率4の端点 $S=0,100$ は0と約0.93999。

非適応対照では各試行の確率を同じ (p) に固定し、成功数上限による切替も除いた。厳密二項和で評価した。

| N | 固定p | 倍率4の失敗確率 | 倍率4で下限が正の確率 |
| --- | --- | --- | --- |
| 100 | 1/1000 | 0.000003631682 | 0.000003631682 |
| 100 | 1/100 | 0.0005345345 | 0.01837404 |
| 1000 | 1/1000 | 0.0005880701 | 0.01892683 |
| 1000 | 1/100 | 0.00004202921 | 0.98992735 |
| 10000 | 1/1000 | 0.00004643922 | 0.98969042 |
| 10000 | 1/100 | 1.575463e−24 | 1.0（表示丸め） |

特に固定 $N=100,p=1/1000$ の対照では、正の下限が出たときは常に真値を超えた。全経路での失敗率は約0.000363%で、1%の保証と両立する。

## 4. 量子予測への接続と範囲

数値対照は [旧KL監査の量子模型](t_search_kl_feedback_audit.md) の第五設定に対応する。フラグ0の操作 $\Phi_{t,0}(\rho)=p_t Z\rho Z$ とフラグ1の $(1-p_t)\rho$ が共通ブロックを構成し、フラグ確率の経路平均は $\mu_N$。量子側への接続には、名目入力の準備誤差上限 $a_*$ を引いた $\max(0,L_4-a_*)$ を分枝確率下限に使う。五設定に各1%を割り当てるなら、例えば第五設定だけ倍率4、四つの正答率は前段の加法法と先に決めて、合併則で同じ経路平均について95%以上の同時被覆を得る。データを見て同じ予算の複数下限から最大値を選ぶ操作はこの証明の範囲外。

＋入力に対する正確率のフラグ0分枝は $Z|+\rangle=|-\rangle$ を返すので、恒等回復からの距離は1。この対照での正の分枝確率下限は、非自明な状態距離保証を意味しない。五設定の全記録による距離保証の発行頻度は未評価。校正予算の独立な根拠、共通ブロック、量子リセット、配線は物理的な適用条件として残る。

全履歴を記述する確率モデルの内部で、記録が後続処理を変え、その同じ経路の予測平均に有限記録から下限を付けられる。ここで精密化したのは予測の保証であり、別の観測者との記録一致は別の検証対象である。記録形成の物理的機構、単一事実の現実化、存在論的becomingについては未決着。

## 5. 再現と検証

リポジトリrootから下の一つのPythonブロックを抽出してファイルに保存し、`python /tmp/feedback_count_check.py` として実行する。Python 3.12.14、NumPy 2.3.5で実行した。NumPyは読み込む凍結済み旧監査で使う。旧報告の境界認証と旧失敗確率の整数分子を再実行し、前向きDPの六分子のhashを照合。質量保存、198件の整数境界と80桁Decimal逆根の一致、全六条件の独立した後向き再帰を確認した。確率の最大絶対差は $8\times10^{-80}$。下表のCIは回帰検証で、この解析の独立査読とは区別する。

| CI | 実際のcheckout | 結果 |
| --- | --- | --- |
| [基点push](https://github.com/kosukeya/t-search/actions/runs/41942447707) | `4e962b9b42918b841e26775737e95cd62e7b5088` | 1424テスト・18サブテスト成功、945.90秒 |
| [基点PR](https://github.com/kosukeya/t-search/actions/runs/41942453451) | `e1cd9375293d626c69e3e365ae933e3e6bb1cdef` | 1424テスト・18サブテスト成功、942.83秒 |

今回のローカル全体pytestは環境にpytestがないため未実行。研究コードの抽出再実行、既存文書チェックとGit差分の検証結果は実行ログに記す。新headのCIはPR本文で基点と分けて追跡する。[実行ログ](t_search_research_log.md)

~~~python
import contextlib
import hashlib
import io
import json
import re
from decimal import ROUND_CEILING, Decimal, localcontext
from fractions import Fraction
from math import comb
from pathlib import Path

CAP = 32
METRICS = ("old_failure", "positive", "failure", "terminal_mass")


def prior_cases():
    report = Path("docs/t_search_kl_feedback_audit.md").read_text()
    code, = re.findall(r"^~~~python\n(.*?)\n~~~[ \t]*$", report, re.M | re.S)
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        exec(compile(code, "frozen_kl_feedback_audit", "exec"), {})
    cases = json.loads(captured.getvalue())["cases"]
    assert [(c["N"], c["p"]) for c in cases] == [
        (n, f"1/{d}") for n in (100, 1000, 10000) for d in (1000, 100)
    ]
    return cases


def exact_cutoff(n, d, s):
    """Largest active duration in [0,n] with strict undercoverage, or -1."""
    lhs = 4**s * (d*n)**n
    left, right = -1, n + 1
    while right - left > 1:
        mid = (left + right) // 2
        if lhs > 100 * (d*n + 3*mid)**n:
            left = mid
        else:
            right = mid
    return left


def decimal_lower(n, s):
    exponent = (Decimal(4).ln() * s - Decimal(100).ln()) / n
    return max(Decimal(0), (exponent.exp() - 1) / 3)


def forward(n, d, old_g, new_g):
    active = [1] + [0] * (CAP - 1)
    absorbed = [0] * len(METRICS)
    denominator, max_count = 1, 0
    for t in range(1, n + 1):
        denominator *= d
        absorbed = [x*d for x in absorbed]
        next_active = [0] * CAP
        for k, mass in enumerate(active):
            if not mass:
                continue
            for s, weight in ((k, mass*(d-1)), (k+1, mass)):
                old_hit = s > 0 and t <= old_g[s]
                if old_hit or s == CAP or t == n:
                    max_count = max(max_count, s)
                    absorbed[0] += weight * old_hit
                    absorbed[1] += weight * (s >= 4)
                    absorbed[2] += weight * (t <= new_g[s])
                    absorbed[3] += weight
                else:
                    next_active[s] += weight
        assert sum(next_active) + absorbed[3] == denominator
        active = next_active
    assert not any(active)
    return absorbed, denominator, max_count


def backward(n, d, old_g, roots):
    """Evaluate terminal rewards with independent Decimal inverse roots."""
    p = Decimal(1) / d
    q = 1 - p
    future = [(Decimal(0),) * len(METRICS)] * CAP
    for t in range(n, 0, -1):
        mu = Decimal(t) / (n*d)
        now = []
        for s in range(CAP + 1):
            hit = s > 0 and t <= old_g[s]
            if t == n or hit or s == CAP:
                now.append(tuple(map(Decimal, (int(hit), int(roots[s] > 0),
                                               int(roots[s] > mu), 1))))
            else:
                now.append(future[s])
        future = [tuple(q*a + p*b for a, b in zip(now[k], now[k+1]))
                  for k in range(CAP)]
    return future[0]


def control(n, d):
    # All n trials use p=1/d, so the failure threshold is monotone in s.
    rhs = 100 * (d+3)**n
    scale = d**n
    lo, hi = 0, n+1
    while hi - lo > 1:
        s = (lo+hi)//2
        if 4**s * scale > rhs:
            hi = s
        else:
            lo = s
    positive = scale - sum(comb(n,k)*(d-1)**(n-k) for k in range(4))
    failure = scale - sum(comb(n,k)*(d-1)**(n-k) for k in range(hi))
    assert 0 <= failure <= positive <= scale and 100*failure <= scale
    if (n, d) == (100, 1000):
        assert failure == positive
    return float(Fraction(positive, scale)), float(Fraction(failure, scale))


def audit():
    rows = []
    maximum_difference = Decimal(0)
    for case in prior_cases():
        n, d = case["N"], int(case["p"].split("/")[1])
        old_g = [0] + case["cutoffs"]
        new_g = [exact_cutoff(n, d, s) for s in range(CAP + 1)]
        roots = [decimal_lower(n, s) for s in range(CAP + 1)]
        for s, (cutoff, root) in enumerate(zip(new_g, roots)):
            scaled = root*n*d
            inverse_cutoff = int(scaled.to_integral_value(rounding=ROUND_CEILING)) - 1
            assert cutoff == min(n, inverse_cutoff), (n, d, s, cutoff, root)
        exact, denominator, max_count = forward(n, d, old_g, new_g)
        old, positive, failure, _ = exact
        old_bytes = old.to_bytes(max(1, (old.bit_length()+7)//8), "big")
        assert hashlib.sha256(old_bytes).hexdigest() == case["numerator_sha256"]
        assert 0 <= failure <= positive <= denominator and 100*failure <= denominator
        # Since log(100)>4, this certifies the additive lower limit is zero.
        assert max_count**2 <= 2*n
        for observed, target in zip(backward(n, d, old_g, roots), exact):
            maximum_difference = max(maximum_difference,
                                     abs(observed - Decimal(target)/Decimal(denominator)))
        assert maximum_difference <= Decimal("1e-50")
        positive_fixed, failure_fixed = control(n, d)
        rows.append(dict(N=n, p=case["p"], old_failure=float(Fraction(old, denominator)),
                         positive=float(Fraction(positive, denominator)),
                         failure=float(Fraction(failure, denominator)),
                         failure_zero=failure == 0,
                         failure_given_positive=float(Fraction(failure, positive)) if positive else None,
                         max_count=max_count, max_lower=float(roots[max_count]),
                         fixed_positive=positive_fixed, fixed_failure=failure_fixed))
    return rows, maximum_difference


with localcontext() as ctx:
    ctx.prec = 80
    rows, difference = audit()
    assert decimal_lower(100, 0) == 0
    assert 0 < decimal_lower(100, 100) < 1
    half = decimal_lower(100, 50)
    half_additive = Decimal("0.5") - (Decimal(100).ln()/200).sqrt()
    assert half < half_additive
    print(json.dumps(dict(cases=rows, max_decimal_error=str(difference),
                          half_count=[float(half), float(half_additive)],
                          all_success=float(decimal_lower(100, 100))), indent=2))
~~~

## 6. 主張台帳

| ID | 主張 | 根拠・範囲 |
| --- | --- | --- |
| FCB-01 | 六条件の方策と倍率4を実行前に固定した | プロトコルと旧失敗分子hashの全一致 |
| FCB-02 | 固定倍率は予測可能二値列の下限を与える | 条件付き正規化、算術・幾何平均、Markov |
| FCB-03 | 正の下限には4成功以上が必要 | 底4・片側予算0.01の式 |
| FCB-04 | 旧KLの主反例で下限が正になる確率は約98.63% | 固定1000試行の全終端質量 |
| FCB-05 | 六条件で全経路の失敗確率は1%以内 | 厳密整数判定、全六条件の後向き照合 |
| FCB-06 | 発行後だけの失敗率は1%を超え得る | 二つの適応条件と固定p対照 |
| FCB-07 | 加法法と比べた優位は条件に依存する | 六制御でのゼロ下限と構成カウント50/100 |
| FCB-08 | フラグ確率と条件付き状態距離の保証は別 | Z分枝の正確率と＋入力の距離1 |
| FCB-09 | 事前指定で五設定の合併則に接続できる | 共通ブロック・校正等の仮定、距離保証の発行頻度は未計算 |
| FCB-10 | 内部記録と全履歴表現を両立させた模型での予測保証である | 観測者間一致・単一事実・存在論的becomingは未解決 |

次は、全体の分枝条件付き距離に要求する誤差と、保証を発行した場合の誤り率を別々に定める。その選択によって必要な統計手順と実機の信頼条件が変わる。
