# 有限カウントからの条件付き予測保証 — 同時下限と偽保証の監査

2026-11-01、finite-counts-v1。[実施仕様](t_search_finite_counts_protocol.md)の一課題を完了した。基点は d0b65de9a673f477e497153ba9529f138210c277。mainはR5cまでで、R5dと後続補足は未マージ[PR #24](https://github.com/kosukeya/t-search/pull/24)にある。同じブランチを継続し、旧証拠・固定仕様・実装・認定器・JSONを保持する。

**結論:** 事前固定した五つの有限バッチから、四正答確率と対象入力の分枝確率の下限を同時に作り、[前回の分枝上限](t_search_branch_bound.md)へ接続できる。α=0.05なら、前提の下で誤った条件付き上限を出す確率を5%以下に抑えられる。有限回の無失敗をそのまま確率1とする代入は正当化できず、許容された対照模型で「誤差0」という偽保証が確率4/27（約14.8%）で出る例を得た。

これは既存の集中不等式と量子性能境界の接続・再現であり、新しい統計定理や物理法則の発見とは扱わない。下記の整数カウント例は**構成例**で、実機測定や1億ショットの実行報告ではない。

## 1. 前回から変える仮定と、固定する窓口

前回は正確な四正答確率から忠実度下限Lを、別途正確な分枝確率pを与え、$d_b\le\min(1,\sqrt{2(1-L)/p})$ を使った。今回はこれらを有限カウントで置き換える。

| バッチ | 入力・スコア | 記録するもの |
| --- | --- | --- |
| z0,z1,x_plus,x_minus | R3と同じ0,1,＋,−の信頼準備と対応する出力測定 | 各固定試行数n_iと非選択の正答回数k_i |
| b | 事前指定した入力ρとフラグb | 全試行数n_bとbの出現回数k_b |

固定量子ビットCPTP、同じフラグ付き処理、信頼準備測定、リセット、設定漏れ・試行選別なしは維持する。**各バッチ内のIID Bernoulli**を追加仮定とする。ρとb、サイズ、失敗予算を観測前に指定し、同じ入力・処理に下限を使う。未知SPAM・ドリフト・設定依存の分枝処理を認定したとはしない。不検出等が二値スコア/固定次元の信頼モデルへ収まらない場合は、全試行を数えるだけで前提が成立したとはせず保証を保留する。

既存[R3認定器](../src/t_search/r3_certificate.py)は exact_probabilities=True を要求する。頻度を正確なBorn確率と宣言して呼び出す方法は採らず、本報告の統計的な下限と解析を別に置く。旧認定器の入力契約や保存結果は変更しない。

## 2. 単一母数の片側下限

$K\sim{\rm Binomial}(n,\pi)$、$x=K/n$。自然対数を使い

$$
{\rm kl}(x\|r)=x\log(x/r)+(1-x)\log((1-x)/(1-r))
$$

とする。0log0は連続な極限で定義する。x>πなら、指数モーメントとMarkovから

$$
\Pr_\pi(K/n\ge x)
\le\inf_{\lambda>0}e^{-n\lambda x}(1-\pi+\pi e^\lambda)^n
=e^{-n\,{\rm kl}(x\|\pi)}. \tag{F1}
$$

0<π<x<1では最小化する $e^\lambda=x(1-\pi)/[\pi(1-x)]$ を代入する。x=1の端点は確率π^nに一致する。π=0,1も直接扱う。

片側失敗予算βに対し、k=0ならℓ=0、k>0なら

$$
{\rm kl}(k/n\|\ell)=\log(1/\beta)/n,\quad 0<\ell<k/n \tag{F2}
$$

の一意な根を使う。k=nなら $\ell=\beta^{1/n}$。固定πについて $\ell(K)>\pi$ となる最小の整数カウントk_*が存在すれば、(F1)をその尾へ適用して $\Pr_\pi(\ell(K)>\pi)\le\beta$。存在しなければその確率は零である。この離散尾の議論が全母数への被覆証明であり、後述の数値格子が一般性の根拠ではない。

## 3. 五母数の同時下限と量子上限への接続

$\beta=\alpha/5$ を事前に配分し、四つのℓ_iとℓ_bを作る。合併則から、五下限が同時に真の確率以下となる確率は少なくとも1−α。**この合併則にバッチ間の独立性は不要**で、個別尾に使うバッチ内の前提は必要である。

$$
L_{\rm low}=\max\!\left(0,\frac{\ell_{z0}+\ell_{z1}+\ell_++\ell_-}{2}-1\right),
\qquad r_{\rm low}=\ell_b. \tag{F3}
$$

同時被覆事象上では、Hofmann/R3の境界により $L_{\rm low}\le F_e$、$r_{\rm low}\le p_b(\rho)$。r_low>0なら

$$
\boxed{
d_b(\rho)\le
U_{\rm counts}:=\min\!\left(1,\sqrt{\frac{2(1-L_{\rm low})}{r_{\rm low}}}\right).
} \tag{F4}
$$

r_low=0なら条件付き主張を保留する。τ以内の予測差が目的なら $U_{\rm counts}\le\tau$ を確認する。上限1しか返らない場合も、回復不能や分枝同定の成功とは扱わない。

被覆は「この固定した測定計画を反復したとき、誤った上限を出す事象の確率≤α」という頻度論的な意味である。観測済みの世界が正しい確率95%、存在論が成立する確率95%、あるいは**上限を発行した場合だけに条件付けた誤認率≤5%**という意味ではない。

また、この保証は一つの事前固定計画についてのもの。通るまで測る任意停止、結果を見てからのb/ρ/設定選択、追加バッチや反復研究を同じαへ無制限に含める使い方は保証しない。必要なら失敗予算の追加配分や時間一様な方法が別途必要だが、本監査では実装していない。

## 4. 頻度をそのまま使う方法の反例

前回の稀な位相反転対照を使う。

$$
K_0=\sqrt{1-q}I,\quad K_1=\sqrt q Z,\quad 0<q<1.
$$

四正答確率は (1,1,1−q,1−q)、＋入力での分枝1の確率q、条件付き出力は−で距離1。各バッチn回、別バッチも独立とする許容例で考える。

全四検査が無失敗、かつフラグバッチで1回以上b=1が出ると、頻度を真値とする代入は $\widehat L=1,\widehat p>0$ から誤差0を出してしまう。この**誤差0の偽保証事象**の確率は

$$
(1-q)^{2n}\{1-(1-q)^n\}=t^2(1-t),\quad t=(1-q)^n.
$$

t=2/3で最大4/27。n=100なら $q=1-(2/3)^{1/100}\approx0.004046442082$ で約0.1481481481となり、5%を超える。これは正しいR3の定理や(F4)の破れではなく、厳密確率という入力契約を有限頻度へ無断で置き換えた方法の失敗である。

同じn=100、四検査全成功の構成カウントでも、今回の方法は次の結果になる。

| 分枝出現回数 | L_low | r_low | 条件付き上限・判定 |
| --- | ---: | ---: | --- |
| 0 | 約0.9099851720 | 0 | 保留。正確率を保証していない |
| 1 | 約0.9099851720 | 約0.0000371090 | 上限1のみ。誤差0とはしない |

この2例が実際に観測されたとは報告していない。与えた整数カウントに対する手続きの動作を照合した。

## 5. 要求誤差0.01に対する構成カウント例

α=0.05、各バッチ同じn、四つの量子検査カウントは全てk=nとする。分枝カウントはn/2またはn/100。一般の装置でこのカウントが得られると仮定したり、必要/最小試行数を求めたのではない。

| 各バッチn | 分枝回数 | L_low | r_low | U_counts | τ=0.01 |
| --- | ---: | ---: | ---: | ---: | --- |
| 1,000 | 500 | 約0.990810835 | 約0.452125019 | 約0.201615427 | 不達 |
| 1,000 | 10 | 約0.990810835 | 約0.003205834 | 1 | 不達 |
| 100,000 | 50,000 | 約0.999907899 | 約0.495201585 | 約0.019286651 | 不達 |
| 100,000 | 1,000 | 約0.999907899 | 約0.009074974 | 約0.142470568 | 不達 |
| 20,000,000 | 10,000,000 | 約0.9999995395 | 約0.4996606930 | 約0.001357692 | 達成 |
| 20,000,000 | 200,000 | 約0.9999995395 | 約0.0099326291 | 約0.009629565 | 達成 |

最後のnは**もし実測するなら計1億試行**に相当する構成例である。本実行で1億ショットを発生させたわけではなく、整数カウントを指定して式を計算した。試行時間・費用の評価や、より効率的な区間/予算配分の最適化はしていない。

全成功でも有限nではℓ=β^(1/n)<1なので、L_low=1にはならない。零の物理誤差を有限の無失敗カウントだけで宣言しないことが、頻度の直接代入との違いである。

## 6. 独立照合・一次資料・実行状態

| 実行済みの監査 | 結果 |
| --- | --- |
| n={8,25,100}、真値j/100、全カウントの二項確率を有理数で総和 | 303件。単一下限の最大失敗確率0.0096717311574016（n=8,π=0.56）≤β=0.01 |
| n=25の三カウント26³通り | 全17,576判定。位相反転模型の5真値で、誤った非自明上限を出す確率を有理数で総和 |
| 上記5真値q={0.01,0.1,1/3,0.5,0.9} | 最大約1.40676e-19（q=1/3）。この有限点を全模型の一般保証としない |
| 下限の数値計算と別実装のDecimal 60桁/110二分 | 145根を照合。数値余裕前の最大差2.220446049250313e-16 |
| 下限への保守的な数値余裕 | 1e-12。今回の全145根で高精度の根以下であることを確認 |
| 構成カウントと端点 | 上記6例＋フラグ0/1の2例。生カウントの修正や無条件成功への選別なし |
| 実行環境・照合許容差 | Python 3.12.14、標準ライブラリのみ。絶対1e-10、相対0 |

二項確率の総和と比較はFractionによる有理数演算で行った。根の計算には浮動小数点のKL反転を使い、1e-12だけ下向きへ戻して高精度の別実装と比較した。この数値余裕はα・被覆率・物理誤差ではない。任意の入力・丸めモードについて形式検証済みの統計ソフトウェアを作った成果ではなく、今回宣言した計算の保守性を照合した成果である。被覆の一般性は§2–3の解析が根拠。

文書から掲載コードを抽出して再実行し、同じ結果を確認した。変更した5文書の相対リンク115件、主張ID12件、表の列数、R3b/R5b/R5cのソースhash19項目・参照JSON hash2項目とstaged whitespaceを照合した。基点699追跡ファイル中696を保持し、変更は既存Markdown 3件への追記と新規Markdown 2件だけ。過去の進捗本文と実行ログも保持した。

2026-11-01に次の一次資料本文を確認した。

| 一次資料 | 確認箇所・本監査との対応 |
| --- | --- |
| Hoeffding, [Probability Inequalities for Sums of Bounded Random Variables](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf), JASA 58 (1963) | printed pp.14–15、式(1.7)–(1.8)、Theorem 1・式(2.1)、端点の説明。スキャン画像を実際に読んだ。(F1)と対応 |
| Hofmann, [Complementary classical fidelities…](https://arxiv.org/pdf/quant-ph/0409083) | 式(14)–(17)。四確率からの非選択忠実度下限を再確認 |

既知の尾境界の反転、合併則、前回の量子上限を組み合わせた。(F2)–(F4)を新発見として数えず、文献全体に対する新規性の網羅的監査も行っていない。

**未実施:** 実機測定・量子装置の認定、準備/測定/配線/IIDの妥当性検証、未知SPAM・ドリフト補正、任意停止/分枝後選択への保証、最適な試行数や割当の探索、物理時計・全体履歴・単一事実の実装。ローカル全体pytestは文書のみの変更なので反復していない。

基点CIはpush [#41151003113](https://github.com/kosukeya/t-search/actions/runs/41151003113)が実際のhead d0b65de9a673f477e497153ba9529f138210c277を検証し、1424テスト・18サブテスト、948.79秒でsuccess。PR [#41151006495](https://github.com/kosukeya/t-search/actions/runs/41151006495)はmainとのmerge ref 82ec274c79e57447f003b22666374623e0ceae7aを検証し、同数、433.55秒でsuccess。今回の文書headのCIは[PR #24](https://github.com/kosukeya/t-search/pull/24)に別記し、基点の成功で代用しない。

### 再現コード

以下をリポジトリルートで一時Pythonファイルとして実行する。外部ライブラリ、乱数サンプル、旧認定器の呼出し、ファイル書込みは不要。全カウント監査と構成例の結果をJSONで標準出力に返す。

~~~python
import json, math, platform
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache
ALPHA, BETA, GUARD = .05, .01, 1e-12
@lru_cache(None)
def raw_lower(k, n):
    assert isinstance(k, int) and isinstance(n, int) and 0 <= k <= n and n > 0
    if k == 0: return 0.
    if k == n: return math.exp(math.log(BETA)/n)
    x, c, lo, hi = k/n, math.log(1/BETA)/n, 0., k/n
    for _ in range(90):
        r = (lo+hi)/2
        d = x*math.log1p((x-r)/r)+(1-x)*math.log1p((r-x)/(1-r))
        if d > c: lo = r
        else: hi = r
    return lo
@lru_cache(None)
def lower(k, n): return max(0., raw_lower(k, n)-GUARD)
def combine(counts):
    assert len(counts) == 5
    ell = [lower(k, n) for k, n in counts]
    L = max(0., math.nextafter(sum(ell[:4])/2-1, -math.inf))
    r = ell[4]
    u = None if r == 0 else min(1., math.nextafter(math.sqrt(2*(1-L)/r), math.inf))
    return dict(L_low=L, p_low=r, distance_upper=u,
                meets_tau_001=u is not None and u <= .01,
                status='withheld' if u is None else 'bounded')
def pmf(n, p):
    return [math.comb(n,k)*p**k*(1-p)**(n-k) for k in range(n+1)]
# Exact rational summation of every binomial outcome, not Monte Carlo.
worst, worst_at, coverage_cases = Fraction(0), None, 0
for n in (8, 25, 100):
    ell = [Fraction.from_float(lower(k, n)) for k in range(n+1)]
    for j in range(101):
        p = Fraction(j, 100)
        masses = pmf(n, p)
        assert sum(masses) == 1
        failure = sum((v for k,v in enumerate(masses) if ell[k] > p), Fraction(0))
        assert failure <= Fraction(1,100)
        coverage_cases += 1
        if failure > worst: worst, worst_at = failure, (n, j)
# Full 26^3 decisions for the flagged-Z physical control (two Z probes are deterministic).
n = 25
bad_events = []
for a in range(n+1):
    for c in range(n+1):
        for b in range(n+1):
            out = combine([(n,n),(n,n),(a,n),(c,n),(b,n)])
            if out['distance_upper'] is not None and out['distance_upper'] < 1:
                bad_events.append((a,c,b))
end_to_end = []
for q in (Fraction(1,100), Fraction(1,10), Fraction(1,3), Fraction(1,2), Fraction(9,10)):
    cx, cb = pmf(n, 1-q), pmf(n, q)
    failure = sum((cx[a]*cx[c]*cb[b] for a,c,b in bad_events), Fraction(0))
    assert failure <= Fraction(1,20)
    end_to_end.append(dict(q=str(q), false_bound_probability=float(failure)))
# Constructed integer transcripts, not experimental or generated shot data.
examples = []
for n in (1000, 100000, 20000000):
    for k in (n//2, n//100):
        examples.append(dict(n_each=n, flag_count=k, total_shots_if_measured=5*n,
                             **combine([(n,n)]*4+[(k,n)])))
edges = [dict(flag_count=k, **combine([(100,100)]*4+[(k,100)])) for k in (0,1)]
assert edges[0]['status'] == 'withheld'
assert examples[-1]['meets_tau_001']
# An independent 60-digit inverse, compared against every computed endpoint.
def decimal_root(k, n):
    with localcontext() as ctx:
        ctx.prec = 60
        if k == 0: return Decimal(0)
        nn, one = Decimal(n), Decimal(1)
        if k == n: return (Decimal('.01').ln()/nn).exp()
        x, c = Decimal(k)/nn, Decimal(100).ln()/nn
        lo, hi = Decimal(0), x
        for _ in range(110):
            r = (lo+hi)/2
            d = x*(x/r).ln()+(one-x)*((one-x)/(one-r)).ln()
            if d > c: lo = r
            else: hi = r
        return lo
keys = [(k,n) for n in (8,25,100) for k in range(n+1)]
keys += [(k,n) for n in (1000,100000,20000000) for k in (n,n//2,n//100)]
max_raw_difference = 0.
for k,n in keys:
    ref = decimal_root(k,n)
    assert Decimal.from_float(lower(k,n)) <= ref
    max_raw_difference = max(max_raw_difference, abs(raw_lower(k,n)-float(ref)))
assert max_raw_difference < GUARD
# Exact algebraic false-zero-claim probability for a naive frequency plug-in.
n = 100
q = -math.expm1(math.log(2/3)/n)
t = (1-q)**n
naive_false_zero = t*t*(1-t)
assert abs(naive_false_zero-4/27) < 1e-12
print(json.dumps(dict(python=platform.python_version(), alpha=ALPHA, beta_each=BETA,
    probability_guard=GUARD, marginal_coverage_cases=coverage_cases,
    worst_marginal_failure=float(worst), worst_marginal_at=worst_at,
    full_count_decisions=26**3, end_to_end=end_to_end, decimal_checks=len(keys),
    max_raw_root_difference=max_raw_difference, naive_q=q,
    naive_false_zero_probability=naive_false_zero, examples=examples, edges=edges), indent=2))
~~~

## 7. 主張台帳・含意・次の判断

| ID | 主張 | 根拠と限界 |
| --- | --- | --- |
| FIN-01 | 有限カウントに厳密Born確率の宣言を流用しない | §1、旧認定器の契約。旧ソースは保持 |
| FIN-02 | KL尾を反転した片側下限に被覆保証がある | (F1)–(F2)と離散尾の証明。固定n・バッチ内IID |
| FIN-03 | 五下限は失敗予算合計αで同時に使える | 合併則、(F3)。五つ以外の選択・反復を自動追加しない |
| FIN-04 | 正のr_lowで条件付き予測上限(F4)へ接続できる | 前回(B3)、同時被覆。発行後だけに条件付けた誤認率とは異なる |
| FIN-05 | r_low=0なら正確率の条件付き主張を保留する | 端点処理。p=0の状態を作らず、未知pを零と断定もしない |
| FIN-06 | 頻度の直接代入は確率4/27で誤差0を偽保証し得る | §4、独立バッチの許容模型での解析。実測率ではない |
| FIN-07 | 有限無失敗カウントから厳密L=1を宣言しない | k=nのℓ=β^(1/n)、§5 |
| FIN-08 | 303周辺分布・17,576判定・5模型真値を独立照合した | 有理数の全和。有限格子を一般証明へ拡張しない |
| FIN-09 | 145根と6構成例＋2端点を検算した | 高精度照合と数値余裕。数値余裕は被覆率でも物理誤差でもない |
| FIN-10 | 固定計画の被覆と任意停止・事後選択は区別する | §1・3。これらの拡張保証は未実施 |
| FIN-11 | 信頼準備測定・同じ処理・IID等は依然前提 | 校正/装置認定が統計計算で不要になったわけではない |
| FIN-12 | 一課題を標準形式の解析と有限カウント監査として完了 | 実測・新法則・一事実の現実化・存在論的becomingは未認定 |

blockness／becomingへの寄与は、全体の量子過程の性能、内部に得られた有限な記録、記録から行う予測、推論手続きの被覆を分け、その間を追加仮定付きで結べた点である。全体履歴を記述できること、記録が形成されること、観測者間で同じ事実を同定すること、予測が安定すること、一事実の現実化を同一視しない。95%という被覆を、Actualityの成立や存在論的becomingの確率へ読み替えない。

**次の判断:** 総括と補足のレビュー・統合。さらに物理的な適用を進めるなら、要求誤差τ・失敗予算α・対象入力/分枝を先に固定し、IID・準備測定校正のどの根拠が実際に得られるかを判断する。本報告の構成カウントをその実証の代わりにはしない。
