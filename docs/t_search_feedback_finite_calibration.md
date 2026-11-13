# 有限校正と本試験への効率の移送

2026-11-13。前回の射影失敗の取り逃がし補正は、全履歴で成り立つ効率下限を所与とした。今回は別の校正バッチから下限を選び、校正から本試験へ効率を移せる条件を明示して合成した。[実行前仕様](t_search_feedback_finite_calibration_protocol.md) · [前回の補正](t_search_feedback_readout_calibration.md)

## 校正と本試験の誤り予算

校正では真の射影失敗を準備でき、固定した $n$ 回の検出ビットは独立な Bernoulli$(p_{\rm cal})$ と仮定する。検出数 $K$ に対し、候補 $h\in\{1/4,1/2,3/4,7/8\}$ の二項上側確率 $P_h(K'\ge K)$ が $0.01$ 以下となる最大の $h$ を選ぶ。候補なしを0とし、本試験では保証を発行しない。二項尾の反転は Clopper–Pearson の原論文 §1–2 に沿う。ここでは候補を事前固定した片側手続きとして使う。[原論文](https://doi.org/10.1093/biomet/26.4.404) · [本文](https://www.barestatistics.nl/uploads/1/1/7/9/11797954/clopper__pearson_1934.pdf)

真値より大きい最小の候補を $h_*$ とする。候補がなければ過大選択は起こらない。二項上側確率は効率について単調増加するため、選択値が真値を超える事象は $h_*$ の採用閾値を越える事象と一致する。その確率は真値の下で $P_{h_*}$ の下より大きくならず、1%以下。候補は同じカウントで入れ子になるため、四候補で1%を再配分する必要はない。

本試験では、校正データを含む過去に対し、真の射影失敗を検出する条件付き効率が全試行で $p_{\rm cal}$ 以上と仮定する。正確な準備とフラグ、固定入力＋、固定長128、量子リセットは前回と共通。校正結果を固定すると、選んだ $h\le p_{\rm cal}$ の下では前回の補正を使える。フラグなし、記録成功、記録失敗に対する倍率は $1,1+h/4,h/4$。その積が25以上なら距離1/2以下の保証を発行する。

真の分枝が未定義か、距離が1/2を超える経路では、条件付き倍率平均の積は1以下になる。これは記録失敗確率が真の失敗確率の $h$ 倍以上であり、前回の算術・幾何平均による証明が適用できるためである。校正結果を含む初期情報で条件付けても、正規化した積の期待値は1なので、この場合の誤発行確率は4%以下。校正で過大な下限を選ぶ確率1%を加え、**校正から本試験までの無条件誤発行は5%以下**になる。本試験は過去に応じて処理を変えてよい。計算対照では校正と本試験の乱数を独立にしたが、合成の証明に必要なのは校正結果で条件付けた本試験での効率下限である。[本試験の証明](t_search_feedback_readout_calibration.md)

## 固定した八条件の結果

候補順の最小検出数は32回で **15, 24, 30, 33**、64回で **25, 42, 57, 62**。33は32回では採用不能を表す。校正が全検出の場合も、32回では3/4、64回では7/8までしか採用しない。

本試験は直前のフラグで次のフラグ確率が1/4または1/2となる前回の方策を使う。分枝はコヒーレントZ回転で、真の失敗率 $\theta$ に対する距離は $\sqrt\theta$。フラグ条件付きの記録失敗率は本試験効率と $\theta$ の積。表の値は厳密な有理数から表示用に丸めた。

| 校正回数 | 校正効率 | 本試験効率 | 真の失敗率 | 下限なしの確率 | 発行確率 | 無条件誤発行 |
| --- | --- | --- | --- | ---: | ---: | ---: |
| 32 | 1 | 1 | 0 | 0 | 0.999932724 | 0 |
| 32 | 3/4 | 3/4 | 0 | 0.000160244 | 0.610565439 | 0 |
| 32 | 1/4 | 1/4 | 3/8 | 0.994036587 | 0.00000136374 | 0.00000136374 |
| 32 | 1 | 1/4 | 3/8 | 0 | 0.177358618 | 0.177358618 |
| 64 | 1 | 1 | 0 | 0 | 0.999985945 | 0 |
| 64 | 3/4 | 3/4 | 0 | 2.57536e−10 | 0.957260099 | 0 |
| 64 | 1/4 | 1/4 | 3/8 | 0.990894807 | 0.00000208202 | 0.00000208202 |
| 64 | 1 | 1/4 | 3/8 | 0 | 0.321280970 | 0.321280970 |

効率が移送できる零誤りの3/4対照では、校正回数を増やすと発行率が61.06%から95.73%に上がる。同じ増加は、校正効率1から本試験効率1/4へ落ちる対照では誤発行を17.74%から32.13%へ増やす。校正値が正確でも、後者では本試験に適用する下限が過大になる。校正効率1の二条件では校正データが同じ全検出列になるため、校正バッチ単体では移送違反を識別できない。真の距離が閾値を超える対照では、発行した場合だけの誤り率は100%になる。5%は全経路の予算である。

## 再現と検証

下の単一Pythonブロックを抽出し、標準ライブラリだけで実行できる。校正の各閾値の両隣の尾確率を検査し、全八条件を有理数で集計した。本試験はフラグ数の分布と条件付き二項和で計算し、同じ128試行について記録失敗率2通りと下限4通りの発行確率を独立な三値整数DPと厳密照合した。量子距離には前回のコヒーレント回転の解析式を使用した。

| 基点CI | 実際のcheckout | 結果 |
| --- | --- | --- |
| [push](https://github.com/kosukeya/t-search/actions/runs/42430902051) | ac97ebaec5237c99b704de446af1a40d1a355900 | 1424テスト・18サブテスト成功、1011.34秒 |
| [PR](https://github.com/kosukeya/t-search/actions/runs/42430906057) | 8783252a62a9ba2845d5af6d3b83a965c4a7d8e8 | 1424テスト・18サブテスト成功、578.43秒 |

~~~python
from collections import defaultdict
from fractions import Fraction as F
from math import comb


def issues(k, bad, eta):
    c = eta / 4
    return ((c.denominator+c.numerator)**(k-bad) * c.numerator**bad
            >= 25 * c.denominator**k)


def flag_counts(n):
    states = {(0, 0): 1}
    for t in range(1, n+1):
        nxt = defaultdict(int)
        for (flag, k), mass in states.items():
            p = 1 + flag
            nxt[0, k] += (4-p)*mass
            nxt[1, k+1] += p*mass
        assert sum(nxt.values()) == 4**t
        states = nxt
    return [F(states.get((0,k),0)+states.get((1,k),0),4**n)
            for k in range(n+1)]


def factorized(flags, observed, eta):
    return sum(mass * sum(comb(k,b)*observed**b*(1-observed)**(k-b)
                          for b in range(k+1) if issues(k,b,eta))
               for k,mass in enumerate(flags))


def direct(n, observed, etas):
    a, d = observed.numerator, observed.denominator
    states = {(0, 0, 0): 1}
    for t in range(1,n+1):
        nxt = defaultdict(int)
        for (flag,k,b), mass in states.items():
            p = 1 + flag
            nxt[0,k,b] += (4-p)*d*mass
            if d>a:
                nxt[1,k+1,b] += p*(d-a)*mass
            if a:
                nxt[1,k+1,b+1] += p*a*mass
        assert sum(nxt.values()) == (4*d)**t
        states = nxt
    return tuple(F(sum(w for (_,k,b),w in states.items() if issues(k,b,e)),(4*d)**n)
                 for e in etas)


FLOORS = (F(1,4), F(1,2), F(3,4), F(7,8))
N = 128


def binomial(n, p):
    return [comb(n,k)*p**k*(1-p)**(n-k) for k in range(n+1)]


def thresholds(n):
    cutoffs = {}
    for floor in FLOORS:
        masses = binomial(n, floor)
        assert sum(masses) == 1
        cutoff = next(k for k in range(1,n+2) if sum(masses[k:]) <= F(1,100))
        assert sum(masses[cutoff-1:]) > F(1,100)
        cutoffs[floor] = cutoff
    return cutoffs


def calibration_weights(n, p, cutoffs):
    weights = defaultdict(F)
    for k, mass in enumerate(binomial(n,p)):
        chosen = max((floor for floor in FLOORS if k >= cutoffs[floor]), default=F(0))
        weights[chosen] += mass
    assert sum(weights.values()) == 1
    assert sum(mass for floor,mass in weights.items() if floor>p) <= F(1,100)
    return weights


flags = flag_counts(N)
conditional_issue = {}
for observed in (F(0), F(3,32)):
    rates = tuple(factorized(flags, observed, floor) for floor in FLOORS)
    assert rates == direct(N, observed, FLOORS)
    conditional_issue[observed] = dict(zip(FLOORS,rates))
    conditional_issue[observed][F(0)] = F(0)

controls = ((F(1),F(1),F(0)), (F(3,4),F(3,4),F(0)),
            (F(1,4),F(1,4),F(3,8)), (F(1),F(1,4),F(3,8)))
assert all(not issues(0,0,floor) for floor in FLOORS)
for n in (32,64):
    cutoffs = thresholds(n)
    print("cutoffs",n,list(cutoffs.values()))
    for cal, live, theta in controls:
        weights = calibration_weights(n, cal, cutoffs)
        issue = sum(mass * conditional_issue[live*theta][floor]
                    for floor,mass in weights.items())
        false_issue = issue if theta > F(1,4) else F(0)
        if cal <= live:
            assert false_issue <= F(1,20)
        print(n,cal,live,theta,*(f"{float(x):.12g}" for x in
                                 (weights[F(0)],issue,false_issue)))
~~~

## 主張台帳

| ID | 主張 | 根拠・範囲 |
| --- | --- | --- |
| FFC-01 | 有限校正で効率下限の過大選択を1%以下に抑える | 固定長、独立な校正ビット、入れ子の二項尾 |
| FFC-02 | 効率を移送できるなら全体の誤発行は5%以下 | 校正と本試験の予算、条件付き正規化 |
| FFC-03 | 校正を増やすと移送違反の対照で誤発行が増える | 32回と64回、同じ128試行の本試験 |
| FFC-04 | 校正バッチだけでは移送違反を識別できない | 同じ校正効率1、異なる本試験効率 |
| FFC-05 | 保証対象は内部記録が支える経路平均の分枝予測 | 実機の移送、観測者間一致、単一事実、存在論は未決着 |

全履歴を表せる模型で、内部記録が後続処理を選ぶ場合にも予測保証を構成できる。今回特定したのは、その保証に必要な校正と本試験の関係である。物理的な記録形成や観測者間の一致は別途検証を要する。単一事実の現実化と存在論的becomingの解釈は未決着で、関係主義・実体主義・両立説の間をこの模型から選ぶ根拠は得られていない。次の判断は、既知の失敗を用意できる根拠と、履歴依存の効率変化を制約する本試験内の独立な対照をどう設計するかである。
