# 射影失敗の取り逃がしに対する同時読出しの保証

2026-11-08。前回の同時読出しを引き継ぎ、準備とフラグを正確としたまま、目標射影の失敗を読み落とす一種類の校正誤差を扱った。許容条件と数値対照は実行前に固定した。[実行前仕様](t_search_feedback_readout_calibration_protocol.md) · [前回の理想読出し](t_search_feedback_joint_readout.md)

## 効率下限による補正

入力と目標は純粋状態 $\rho_+=|+\rangle\langle+|$。過去の記録を条件とした対象フラグ確率を $p_t$、対象フラグと真の射影失敗の同時確率を $e_t$、対象フラグと**記録上の**失敗の同時確率を $\widetilde e_t$ とする。フラグは正しく、失敗検出効率には全ての試行・過去に共通する下限 $\eta\in(0,1]$ があると仮定する。このとき $\widetilde e_t\ge\eta e_t$。真の成功を失敗と記録しても不等式は成り立つ。記録の欠落とフラグの誤分類は含めない。効率下限は同じ検証データから推定した値ではなく、独立に正当化できる決定論的な制約を仮定する。

バーは固定長 $N$ の同じ実現経路に沿う予測可能平均を表す。$\bar p>0$ のとき、平均分枝を正規化した状態 $\sigma$ と $\rho_+$ の距離は $D(\sigma,\rho_+)\le\sqrt{\bar e/\bar p}$。Fuchs–van de Graaf原論文 Theorem 1、式(46)の上界で、純粋目標に対するroot fidelityの二乗は $\operatorname{Tr}(\rho_+\sigma)$。[著者論文](https://arxiv.org/pdf/quant-ph/9712042)

$c=\eta/4$ と置き、各試行の重み $W_t$ をフラグなしで1、フラグ付き記録成功で $1+c$、フラグ付き記録失敗で $c$ とする。条件付き平均は $m_t=1+cp_t-\widetilde e_t>0$ であり、$M_N=\prod_t W_t/m_t$ は前回と同じ条件付き正規化により期待値1を持つ。対象距離が1/2を超える経路では $\bar e>\bar p/4$ なので、$\overline{\widetilde e}\ge c\bar p$。分枝が未定義の $\bar p=0$ でも $\overline{\widetilde e}\ge c\bar p$。これらの経路では算術・幾何平均不等式より

$$
\prod_t m_t\le(1+c\bar p-\overline{\widetilde e})^N\le1.
$$

従って $\prod_t W_t\ge20$ で発行すると、誤発行事象は $M_N\ge20$ に含まれ、その**全経路での確率は5%以下**。$\eta=1$ では前回の倍率に戻る。全試行がフラグなしなら積は1で発行しない。失敗ゼロのときに必要なフラグ付き成功は $\eta=1$ で14回、$\eta=1/4$ で50回。既知の条件付き正規化をこの校正制約に適用したものである。

## 適応対照と識別不能

直前のフラグ記録で次試行の $p_t$ が $1/4$ または $1/2$ になる前回の方策を維持した。フラグ付き出力には前回のコヒーレントZ回転を使い、真の失敗率 $\theta$ に対する距離は $\sqrt\theta$。記録失敗率はフラグ条件付きで実効効率と $\theta$ の積。数値対照では成功側の誤分類を0とした。表は有理数の発行確率を表示用に丸めた値。

| N | 真の失敗率 | 実効効率 | 下限η | 未補正 | 補正 |
| --- | --- | --- | --- | ---: | ---: |
| 64 | 0 | 1 | 1 | 0.949622208 | 0.949622208 |
| 64 | 0 | 1/4 | 1/4 | 0.949622208 | 1.34421931e−8 |
| 64 | 3/8 | 1/4 | 1/4 | 0.271429670 | 9.42806207e−11 |
| 64 | 3/32 | 1 | 1/4 | 0.271429670 | 9.42806207e−11 |
| 128 | 0 | 1 | 1 | 0.999999082 | 0.999999082 |
| 128 | 0 | 1/4 | 1/4 | 0.999999082 | 0.156377616 |
| 128 | 3/8 | 1/4 | 1/4 | 0.527227928 | 0.000862026157 |
| 128 | 3/32 | 1 | 1/4 | 0.527227928 | 0.000862026157 |

真の失敗率3/8では距離 $\sqrt{3/8}>1/2$ なので発行は全て誤り。128試行で未補正は52.72%の誤発行、補正は0.0862%。補正しても、この装置で発行した場合だけの誤り率は100%。真の失敗率0で効率下限1/4を使う場合、128試行の発行率は15.64%に留まる。

失敗率3/8・効率1/4と失敗率3/32・効率1は、共通の下限1/4の下で記録失敗率がともに3/32。フラグ過程も等しく、従って適応制御を含む全記録分布が等しい。しかし後者の距離は $\sqrt{3/32}<1/2$。この測定だけを用い、悪い方で誤発行を5%以内にするどんな判定も、良い方での発行確率は5%以下になる。これは採用した倍率固有の限界とは別で、同じ情報から装置を識別できないことによる。

## 再現・範囲

下のコードを抽出してPythonで実行する。八条件をフラグ数の整数DPと条件付き二項和で厳密に計算した。N=64の四条件について別の三値整数DPで、未補正・補正とも厳密一致。過程は質量保存、零フラグの不発行、η=1の復元を確認した。量子側は前回のZ回転の解析式を用いる。今回の検証は数値対照と解析で、物理的な装置校正は未実施。

| 基点CI | 実際のcheckout | 結果 |
| --- | --- | --- |
| [push](https://github.com/kosukeya/t-search/actions/runs/42317263556) | f2d7ef2c019b0f2d354739d78eadd837cb465beb | 1424テスト・18サブテスト成功、590.02秒 |
| [PR](https://github.com/kosukeya/t-search/actions/runs/42317268301) | 27d28826ed5e1cfa0d2223e7ebc31a7cc8dbff5f | 1424テスト・18サブテスト成功、582.32秒 |

~~~python
from collections import defaultdict
from fractions import Fraction as F
from math import comb


def issues(k, bad, eta):
    c = eta / 4
    return ((c.denominator+c.numerator)**(k-bad) * c.numerator**bad
            >= 20 * c.denominator**k)


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


conditions = ((F(0),F(1),F(1)), (F(0),F(1,4),F(1,4)),
              (F(3,8),F(1,4),F(1,4)), (F(3,32),F(1),F(1,4)))
for n in (64,128):
    flags = flag_counts(n)
    rows = []
    for theta, efficiency, floor in conditions:
        assert efficiency >= floor
        etas = (F(1), floor)
        observed = theta * efficiency
        pair = tuple(factorized(flags,observed,e) for e in etas)
        if n == 64:
            assert pair == direct(n,observed,etas)
        if theta > F(1,4):
            assert pair[1] <= F(1,20)
        rows.append(pair)
        print(n,theta,efficiency,floor,*(f"{float(x):.12g}" for x in pair))
    assert rows[2] == rows[3]
assert all(not issues(0,0,eta) for eta in (F(1),F(1,4)))
assert [next(k for k in range(128) if issues(k,0,e)) for e in (F(1),F(1,4))] == [14,50]
~~~

## 主張台帳

| ID | 主張 | 根拠・範囲 |
| --- | --- | --- |
| FRC-01 | 効率下限により真の失敗率と効率下限から記録失敗率を下から評価できる | 正確なフラグ、後段の古典的読出し |
| FRC-02 | 補正則は全経路の誤発行を5%以下に抑える | 固定長、既知下限、条件付き正規化とMarkov |
| FRC-03 | 未補正では128試行の反例で52.72%誤発行する | 八条件の厳密計算、補正では0.0862% |
| FRC-04 | 効率下限が弱い場合は良好な装置でも発行頻度が下がる | 真の失敗率0で128試行の対照 |
| FRC-05 | 同一の全記録分布で距離の閾値判定が異なる | 共通下限1/4、指定の読出しと制御 |
| FRC-06 | 対象は全履歴の中の記録が支える分枝平均の予測 | 観測者間一致、単一事実の現実化、存在論的becomingとは区別 |

全履歴の確率モデルに内部記録と後続制御を共存させても、その記録を理想の測定結果として読むには装置の情報が要る。今回の結果は許容された予測操作の保証を限定し、物理的な記録形成や観測者間の同一事実を検証したものではない。次は効率下限を独立に検証できる測定と、対象外にしたフラグ誤分類・準備誤差をどう制約するかを判断する。
