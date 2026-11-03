# 校正誤差予算と条件付き予測 — 統計を増やしても残る制約

日付: 2026-11-02（Asia/Tokyo）。[実行前プロトコル](t_search_calibration_budget_protocol.md)の一課題を完了した。基点は [50f27e6f0762966570910df6564cc4a6c26a3839](https://github.com/kosukeya/t-search/commit/50f27e6f0762966570910df6564cc4a6c26a3839)、同じ research/r5d-synthesis・[Draft PR #24](https://github.com/kosukeya/t-search/pull/24)を継承する。mainのR5c統合は [4a0f32d8fdd87f7daa6a3f0a9cac4c81b6fac5c2](https://github.com/kosukeya/t-search/commit/4a0f32d8fdd87f7daa6a3f0a9cac4c81b6fac5c2)のまま。今回まで外部更新・レビュー追加はない。

**結論:** 外部に根拠のある準備・測定の誤差上限を、前回の五つの有限カウント下限へ保守的に合成できる。ただし校正上限をこのデータだけから認定したわけではない。無校正では、同じ全成功記録と整合する恒等処理とZ位相反転があり、理想入力の条件付き距離は0と1に分かれる。回数を増やすだけでこの識別不能は解消しない。

## 1. 問い・対象・今回緩めた仮定

[前回の有限カウント報告](t_search_finite_counts.md)の信頼準備測定を、**既知の校正誤差予算**へ置き換える。同じ[分枝上限](t_search_branch_bound.md)を使い、IID、固定計画、同一チャネル・次元・配線・リセット・設定漏れ/試行選別なしは維持する。これらの実機検証は行っていない。

量子ビットの固定CPTPチャネルをΛ、完備なインストゥルメントを{Φ_b}、Σ_b Φ_b=Λとする。実際の公開フラグbがΦ_bを定義する。bを原模型のF1のZ記録や未観測の「理想の事実」へ同一視しない。誤ラベルがある装置も、その公開ラベルで定義された実際の操作に対する主張に限る。未登録の欠落・選別を認める変更ではない。

四検査j=0,1,＋,−の名目入力ρ_j、名目の正答効果M_j=ρ_jに対し、実際の固定入力σ_jと効果\(\widetilde M_j\)について

\[
D(\sigma_j,\rho_j)\le a_j,\qquad
\|\widetilde M_j-M_j\|_\infty\le m_j,\qquad
0\le\widetilde M_j\le I
\tag{K1}
\]

を仮定する。Dは半トレースノルム。a_j,m_jは別の根拠で正当化された上限を**仮定**し、今回のカウントから推定しない。実際の四正答率は
\(\widetilde\pi_j=\operatorname{Tr}\widetilde M_j\Lambda(\sigma_j)\)。
理想基準で評価したい率は
\(\pi_j=\operatorname{Tr}M_j\Lambda(\rho_j)\)である。

対象フラグのバッチも、名目ρと実際の固定σを分け、
\(D(\sigma,\rho)\le a_*\)とする。五つ目のカウントが測るのは **p_b(σ)**。前回の対象は理想入力の

\[
d_{\rm ideal}=D\!\left(\Phi_b(\rho)/p_b(\rho),\rho\right).
\]

実際に準備した入力から名目目標までの距離
\(d_{\rm actual}=D(\Phi_b(\sigma)/p_b(\sigma),\rho)\)
は別の量である。後者は同じ導出の系として明記し、今回の問いを二つに増やさない。

## 2. 誤差予算を合成する導出

任意の効果0≤M≤Iについて、確率差はD以下。従って

\[
\begin{aligned}
|\widetilde\pi_j-\pi_j|
&\le |\operatorname{Tr}(\widetilde M_j-M_j)\Lambda(\sigma_j)|
 +|\operatorname{Tr}M_j\Lambda(\sigma_j-\rho_j)|\\
&\le m_j+D(\Lambda(\sigma_j),\Lambda(\rho_j))
 \le m_j+a_j .
\end{aligned}
\tag{K2}
\]

第一項は作用素ノルムと状態のトレース1、第二項は二値測定、最後はCPTP写像の距離収縮による。未知Λを同定する必要はない。

前回の片側KL下限ℓ_jは\(\widetilde\pi_j\)の下限である。同時被覆事象上では

\[
s_j=\max(0,\ell_j-a_j-m_j)\le\pi_j,\qquad
L_{\rm cal}=\max\!\left(0,\frac{\sum_js_j}{2}-1\right)\le F_e(\Lambda).
\tag{K3}
\]

\(F_e=\langle\Omega|(\Lambda\otimes{\rm id})(|\Omega\rangle\langle\Omega|)|\Omega\rangle\)
は恒等目標のBell重なりであり、平均出力忠実度とは別。最後の不等式は、名目のZ/Xという相補基底に対するHofmannの下限を使う。実際の軸が相補的だと再仮定していない。

分枝の効果\(E_b=\Phi_b^*(I)\)は0≤E_b≤Iなので、
\(|p_b(\sigma)-p_b(\rho)|\le a_*\)。五つ目の下限ℓ_bから

\[
r_{\rm ideal}=\max(0,\ell_b-a_*),\qquad
U_{\rm ideal}=\min\!\left(1,\sqrt{\frac{2(1-L_{\rm cal})}{r_{\rm ideal}}}\right)
\tag{K4}
\]

を得る。本手続きではr_ideal>0のときだけ理想入力の正確率分枝を主張し、
\(d_{\rm ideal}\le U_{\rm ideal}\)。
r_ideal=0では保留し、確率零を断定せず、零確率状態も正規化しない。

一方、ℓ_b>0なら前回の上限をσに適用して三角不等式を使うと、

\[
d_{\rm actual}\le
U_{\rm actual}
=\min\!\left(1,a_*+\sqrt{\frac{2(1-L_{\rm cal})}{\ell_b}}\right).
\tag{K5}
\]

ℓ_b=0ならこちらも保留。(K4)と(K5)の対象を混ぜない。実際の分枝に正の確率が示せても、準備誤差の範囲にある理想入力の同じ分枝に正の確率が示せるとは限らない。

前回と同じα=0.05、各母数へのβ=0.01を使う。五つの片側下限の同時被覆は少なくとも1−αであり、(K1)が決定論的に成り立つなら補正はその事象上で全て成立する。従って固定計画における偽保証事象の無条件確率はα以下。別途校正を推定した場合の失敗確率はここに含めていない。保証発行後だけに条件付けた誤認率、事後確率、任意停止・分枝後選択・繰返し全体への95%保証ではない。

## 3. 固定した24例と対象入力の3例

前回と同じ、四検査の全n回成功・フラグ回数kという**構成カウント**を使う。各検査でa_j=m_j=η/2、a_*=0。表のp下限は実際/理想入力で共通、Uは(K4)。四つのηと六つのカウント条件の24例を全て計算した。各バッチnであり、実測した総5nショットではない。

| n（各バッチ） | k | p下限 | U: η=0 | η=10^-8 | η=10^-6 | η=10^-4 |
| --- | --- | --- | --- | --- | --- | --- |
| 1000 | 500 | 0.4521250193 | 0.2016154269 | 0.2016156463 | 0.2016373662 | 0.2037976727 |
| 1000 | 10 | 0.0032058337 | 1 | 1 | 1 | 1 |
| 100000 | 50000 | 0.4952015846 | 0.0192866514 | 0.0192887453 | 0.0194949337 | 0.0343471509 |
| 100000 | 1000 | 0.0090749737 | 0.1424705680 | 0.1424860361 | 0.1440091503 | 0.2537225367 |
| 20000000 | 10000000 | 0.4996606930 | 0.0013576917 | 0.0013868602 | 0.0031382733 | 0.0283264291 |
| 20000000 | 200000 | 0.0099326291 | 0.0096295645 | 0.0098364447 | 0.0222585181 | 0.2009080384 |

τ=0.01なら、n=20000000・k=200000はη=0,10^-8で保証でき、η=10^-6,10^-4ではこの十分上限が条件を満たさない。保証できないことを実際の誤差がτを超えた証拠と解釈しない。零予算と旧コードの上限の最大差は1.17e-12未満で、丸め方の差に留まる。

同じn=20000000・k=200000、四検査のη=0のまま、対象準備のa_*だけを変えた。

| a_* | r_ideal | U_ideal | U_actual |
| --- | --- | --- | --- |
| 0 | 0.0099326291 | 0.0096295645 | 0.0096295645 |
| 0.005 | 0.0049326291 | 0.0136646819 | 0.0146295645 |
| 0.01 | 0 | 保留 | 0.0196295645 |

最後の行は「実際に準備したσの分枝」についての上限を残すが、理想ρの正確率分枝については保留する。どちらも理想入力を実際に準備できた証明ではない。

### 無限カウントでも消えない、この保証式の床

統計誤差が消えて実際の四正答率が全て1、分枝確率r>0、a_*=0、各a_j+m_j=η≤1/2なら、

\[
L_{\rm cal}=1-2\eta,\qquad
U_\infty=\min(1,\sqrt{4\eta/r}).
\tag{K6}
\]

η=10^-4、r=0.01ではU_∞=0.2。この十分保証でτ=0.01を満たすにはη≤rτ²/4=2.5×10^-7が必要。これは**この上限を使う証明手続きの条件**であり、装置の実際の誤差が0.2以上になる、全ての推定法でこれ以上良くできない、という物理的/最適性の主張ではない。準備・測定の別々の誤差を合計だけで扱うため緩い場合もある。有限計算の1e-12数値余裕とは区別した解析上の極限である。

## 4. 無校正での識別不能 — 相補性を失う対照

Z検査は本来の|0>,|1>のまま、名目X検査だけを

\[
\sigma_\pm(\theta)=\widetilde M_\pm(\theta)
=\frac{I\pm(\cos\theta X+\sin\theta Z)}{2},\quad 0\le\theta\le\pi/2
\tag{K7}
\]

にする。準備距離と効果ノルム差は、どちらもsin(θ/2)。処理は設定で切替えず、装置Aは恒等チャネルI、装置Bは固定Zチャネル。公開フラグは一つで常に発生する。未知の入力ラベルを装置へ漏らす仕組みはない。

Z正答率は両装置で1。Xと呼ぶ二設定の実際の正答率はAで1、Bでsin²θ。Bを誤って完全校正と扱うと、素朴な忠実度下限はsin²θになるが、本来の恒等目標に対するF_e(Z)=0である。(K3)はこの対照でBの下限を全て0へ戻す。

| θ | a_±=m_± | Bの実際X正答率 | 補正L: A | 補正L: B | D(実際出力,名目＋): A | 同: B |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| π/12 | 0.1305261922 | 0.0669872981 | 0.7389476156 | 0 | 0.1305261922 | 0.9914448614 |
| π/4 | 0.3826834324 | 0.5 | 0.2346331353 | 0 | 0.3826834324 | 0.9238795325 |
| π/2 | 0.7071067812 | 1 | 0 | 0 | 0.7071067812 | 0.7071067812 |

θ=π/2では、名目X二設定が実際にはZ二設定へ崩れ、AとBの**全五確率が(1,1,1,1,1)で一致**する。有限でも無限回でも、この記録だけでA/Bを識別できない。一方、理想＋入力での距離はAで0、Bで1、Bell重なりは1と0。理想＋の出力をこのデータから認定することはできない。

実際の対象準備をσ_+(θ)とすれば、出力と名目＋の距離はAでsin(θ/2)、Bでcos(θ/2)。θ=π/2で実際に「＋から−への変化を観測した」とは言えず、両装置とも実際には|0>を入出力する。この区別が(K4)/(K5)を分ける理由である。

この対照は、Z軸を固定したまま**相対的な検査軸の相補性を失わせる**。全てを同じユニタリで回転する単なる基準座標のゲージとは異なる。[R3の信頼条件監査](t_search_r3_synthesis.md)が既に区別した校正と実装同定の論点を具体化したのであり、SPAMの問題を今回初めて発見したとは主張しない。

## 5. 検証・一次資料・実施しなかったこと

Python 3.12.14、NumPy 2.3.5で、プロトコルの全24+3例・8行列ケースを実行した。行列からの準備距離・効果ノルム・正答率・Bell状態によるF_e・二種の出力距離を、独立な解析式と照合した。93数値等式と56不等式を確認し、最大等式残差と数値的な不等式超過は共に3.34e-16未満。一般保証は§2の解析であり、この有限走査が全CPTP写像を尽くすわけではない。

35ケース全ての補正式を80桁Decimalの別実装と比較し、下限は参照値以下、上限は参照値以上、最大差1.03e-12未満を確認した。最初の試作では全演算へ一律nextafterを使い、L=1の厳密端点でも上限3.3320009373e-8を生じ、1e-10の近接照合に失敗した。危険側への破れではなかったが、最終コードは線形補正を有理数で評価し、必要なときだけ保守側へ丸め、厳密端点を保持する。失敗を許容差変更や解析値の書換えで通過させていない。

前回報告のコードを変更せず読み込んで再実行し、303件の有理数二項被覆、17,576判定・5模型確率、145高精度根も再確認した。掲載コードを抽出した再実行と、文書・相対リンク・台帳・旧blob/hash保持の検証は実行ログに記録する。丸めチェックは今回の宣言条件の検算であり、任意入力に対する形式検証済みの認定ソフトウェアを新設したわけではない。

既存の文書整合性チェック30ファイルの、標準ライブラリだけで独立に呼べる196個のassertion関数を直接実行して全て成功した。pytest未導入のこのローカル環境でpytest suiteを実行したとの意味ではなく、他モジュールに依存する3ファイルと全体回帰は対象外。完全な回帰CIは下記の正確なheadで区別する。

2026-11-02に次の一次資料本文を確認した。

| 一次資料 | 確認した箇所と使用範囲 |
| --- | --- |
| Hofmann, [Complementary classical fidelities…](https://arxiv.org/pdf/quant-ph/0409083) | 式(6)の相補性、式(14)–(17)、特に(15)。名目Z/X率からのBell忠実度下限 |
| Watrous, [The Theory of Quantum Information](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf)（著者公開稿） | printed p.130 Proposition 3.5・(3.21)–(3.23)、p.168 Corollary 3.40・(3.241)。測定確率差とトレース距離、チャネルの収縮 |

(K2)–(K6)は既知のノルム不等式、Hofmann下限、前二報の保証の合成として提示する。最良定数・新規理論・新法則とは主張せず、網羅的な新規性調査も実施していない。

**未実施:** 実機測定、(K1)を実証する独立校正、未知SPAMやドリフトの推定、IID/配線/資源の認定、校正上限自体の信頼区間と失敗予算、任意停止・事後選択への拡張、GSTや新認定器、全体履歴・時計・単一事実の実装。旧認定器のexact_probabilities契約、ソース・テスト・数値JSONを変更していない。文書のみなのでローカル全体pytestは反復せず、掲載解析を実行した。

基点push [#41258997043](https://github.com/kosukeya/t-search/actions/runs/41258997043)は実際のcheckout 50f27e6f0762966570910df6564cc4a6c26a3839で1424テスト・18サブテスト、948.84秒、success。基点PR [#41259001047](https://github.com/kosukeya/t-search/actions/runs/41259001047)はmerge ref df53e8284396cca3bcc2b564c9df0a3ce262d2faで同数、947.48秒、success。今回のheadのCIは別に[PR #24](https://github.com/kosukeya/t-search/pull/24)へ記録し、これら基点の成功で代用しない。

### 再現コード

リポジトリルートで次のブロックを一時Pythonファイルとして実行する。依存は標準ライブラリとNumPy（既存依存）。ファイル書込み、乱数、旧認定器の呼出し、実機ショットは不要。前回の有限カウント監査を先にそのまま実行する。全構成結果と検証要約をJSONで標準出力へ返す。

~~~python
import contextlib, io, json, math, platform
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import numpy as np

# Re-run the frozen finite-count audit; do not alter or call the R3 certifier.
old_source = Path('docs/t_search_finite_counts.md').read_text().split('~~~python\n')[1].split('\n~~~')[0]
old, captured = {}, io.StringIO()
with contextlib.redirect_stdout(captured):
    exec(compile(old_source, 'frozen_finite_counts_report', 'exec'), old)
prior = json.loads(captured.getvalue())
lower, old_combine = old['lower'], old['combine']
TOL = 1e-10
down = lambda x: math.nextafter(x, -math.inf)
up = lambda x: math.nextafter(x, math.inf)

def branch_bound(L, r):
    if r <= 0: return None
    if L == 1: return 0.
    return min(1., up(math.sqrt(up(up(2*up(1-L))/r))))

def rational_down(q):
    f = float(q)
    return down(f) if Fraction.from_float(f) > q else f

def corrected(ell, a, m, target_a=0.):
    assert len(ell) == 5 and len(a) == len(m) == 4
    assert all(0 <= v <= 1 for v in [*ell, *a, *m, target_a])
    E,A,M = [[Fraction.from_float(x) for x in seq] for seq in (ell,a,m)]
    scores = [max(Fraction(0),e-x-y) for e,x,y in zip(E[:4],A,M)]
    L = rational_down(max(Fraction(0),sum(scores)/2-1))
    r = rational_down(max(Fraction(0),E[4]-Fraction.from_float(target_a)))
    ideal = branch_bound(L, r)
    actual0 = branch_bound(L, ell[4])
    actual = None if actual0 is None else (actual0 if target_a == 0 else min(1., up(actual0+target_a)))
    return dict(L=L, r_ideal=r, U_ideal=ideal, U_actual=actual,
                meets_tau_001=ideal is not None and ideal <= .01)

# Independent 80-digit evaluation of the algebra using the exact binary inputs.
def decimal_reference(ell, a, m, target_a):
    with localcontext() as ctx:
        ctx.prec = 80
        E,A,M = [[Decimal.from_float(x) for x in seq] for seq in (ell,a,m)]
        t, z, one = Decimal.from_float(target_a), Decimal(0), Decimal(1)
        scores = [max(z,e-x-y) for e,x,y in zip(E[:4],A,M)]
        L, r = max(z,sum(scores)/2-1), max(z,E[4]-t)
        ideal = None if r == 0 else min(one,(2*(1-L)/r).sqrt())
        actual = None if E[4] == 0 else min(one,t+(2*(1-L)/E[4]).sqrt())
        return dict(L=L, r_ideal=r, U_ideal=ideal, U_actual=actual)

rounding_checks, max_round_difference = 0, 0.
def audit_rounding(ell, a, m, target_a):
    global rounding_checks, max_round_difference
    out, ref = corrected(ell,a,m,target_a), decimal_reference(ell,a,m,target_a)
    for key in ('L','r_ideal','U_ideal','U_actual'):
        if ref[key] is None:
            assert out[key] is None
            continue
        v = Decimal.from_float(out[key])
        assert v <= ref[key] if key in ('L','r_ideal') else v >= ref[key]
        max_round_difference = max(max_round_difference,abs(out[key]-float(ref[key])))
    rounding_checks += 1
    return out

examples, target_examples, max_zero_budget_difference = [], [], 0.
for n in (1000,100000,20000000):
    for k in (n//2,n//100):
        counts = [(n,n)]*4+[(k,n)]
        ell = [lower(kj,nj) for kj,nj in counts]
        for eta in (0.,1e-8,1e-6,1e-4):
            out = audit_rounding(ell,[eta/2]*4,[eta/2]*4,0.)
            examples.append(dict(n_each=n,flag_count=k,eta=eta,**out))
            if eta == 0:
                baseline = old_combine(counts)
                max_zero_budget_difference = max(max_zero_budget_difference,
                    abs(out['U_ideal']-baseline['distance_upper']))
                assert abs(out['U_ideal']-baseline['distance_upper']) < TOL
ell = [lower(20000000,20000000)]*4+[lower(200000,20000000)]
for target_a in (0.,.005,.01):
    out = audit_rounding(ell,[0.]*4,[0.]*4,target_a)
    target_examples.append(dict(target_a=target_a,**out))
assert target_examples[-1]['U_ideal'] is None
assert target_examples[-1]['U_actual'] is not None

# Independent matrix calculations, with fixed true Z settings and tilted X settings.
I = np.eye(2,dtype=complex)
X = np.array([[0,1],[1,0]],complex)
Z = np.diag([1.,-1.]).astype(complex)
nominal = [(I+Z)/2,(I-Z)/2,(I+X)/2,(I-X)/2]
bell = np.array([1,0,0,1],complex)/math.sqrt(2)
bell_state = np.outer(bell,bell.conj())
distance = lambda r,s: float(np.abs(np.linalg.eigvalsh(r-s)).sum()/2)
opnorm = lambda h: float(np.abs(np.linalg.eigvalsh(h)).max())
max_matrix_residual, max_inequality_excess, scalar_checks, inequality_checks = 0., 0., 0, 0
def equal(x,y):
    global max_matrix_residual, scalar_checks
    error = abs(float(x)-float(y))
    max_matrix_residual = max(max_matrix_residual,error)
    scalar_checks += 1
    assert error < TOL
def below(x,y):
    global max_inequality_excess, inequality_checks
    inequality_checks += 1
    max_inequality_excess = max(max_inequality_excess,float(x-y))
    assert x <= y+TOL

matrix_cases = []
for theta in (0.,math.pi/12,math.pi/4,math.pi/2):
    axis = math.cos(theta)*X+math.sin(theta)*Z
    prepared = nominal[:2]+[(I+axis)/2,(I-axis)/2]
    effects = prepared
    a = [distance(s,r) for s,r in zip(prepared,nominal)]
    m = [opnorm(e-r) for e,r in zip(effects,nominal)]
    expected_errors = [0.,0.,math.sin(theta/2),math.sin(theta/2)]
    for x,y in zip(a+m,expected_errors*2): equal(x,y)
    for label,U in (('I',I),('Z',Z)):
        outputs = [U@s@U.conj().T for s in prepared]
        observed = [float(np.trace(e@s).real) for e,s in zip(effects,outputs)]
        ideal_scores = [float(np.trace(r@U@r@U.conj().T).real) for r in nominal]
        expected = [1.,1.]+([1.,1.] if label == 'I' else [math.sin(theta)**2]*2)
        for x,y in zip(observed,expected): equal(x,y)
        for x,y,aa,mm in zip(observed,ideal_scores,a,m): below(abs(x-y),aa+mm)
        J = np.kron(U,I)@bell_state@np.kron(U,I).conj().T
        Fe = float(np.vdot(bell,J@bell).real)
        equal(Fe,1. if label == 'I' else 0.)
        ideal_d = distance(U@nominal[2]@U.conj().T,nominal[2])
        actual_d = distance(outputs[2],nominal[2])
        equal(ideal_d,0. if label == 'I' else 1.)
        equal(actual_d,math.sin(theta/2) if label == 'I' else math.cos(theta/2))
        target_a = a[2]
        # Single public flag always occurs. No hidden ideal-label identification.
        ell_model = expected+[1.]  # Analytic scores; retain raw matrix values above.
        out = audit_rounding(ell_model,a,m,target_a)
        below(out['L'],Fe)
        if out['U_ideal'] is not None: below(ideal_d,out['U_ideal'])
        below(actual_d,out['U_actual'])
        matrix_cases.append(dict(theta_over_pi=theta/math.pi,channel=label,
            observed=observed+[1.],Fe=Fe,naive_L=sum(observed)/2-1,
            ideal_distance=ideal_d,actual_to_nominal_distance=actual_d,**out))
equal(max(abs(x-y) for x,y in zip(matrix_cases[-2]['observed'],matrix_cases[-1]['observed'])),0.)
equal(matrix_cases[-2]['Fe']-matrix_cases[-1]['Fe'],1.)
equal(matrix_cases[-1]['ideal_distance']-matrix_cases[-2]['ideal_distance'],1.)
assert max_round_difference < TOL

eta, mass, tau = 1e-4,.01,.01
floor = min(1.,math.sqrt(4*eta/mass))
budget_for_tau = mass*tau*tau/4
equal(floor,.2)
equal(budget_for_tau,2.5e-7)
print(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,
    reused_prior=dict(marginal_coverage_cases=prior['marginal_coverage_cases'],
        full_count_decisions=prior['full_count_decisions'],decimal_checks=prior['decimal_checks']),
    count_examples=examples,target_examples=target_examples,matrix_cases=matrix_cases,
    matrix_scalar_checks=scalar_checks,matrix_inequality_checks=inequality_checks,max_matrix_residual=max_matrix_residual,
    max_inequality_excess=max_inequality_excess,rounding_cases=rounding_checks,
    max_round_difference=max_round_difference,max_zero_budget_difference=max_zero_budget_difference,
    infinite_count_certificate_floor=floor,eta_needed_for_tau=budget_for_tau),indent=2))
~~~

## 6. 主張台帳・blockness／becomingへの含意

| ID | 主張 | 根拠と限界 |
| --- | --- | --- |
| CAL-01 | 今回緩めた仮定は既知の準備・測定誤差予算 | §1、(K1)。外部校正の実証や未知SPAM推定は未実施 |
| CAL-02 | 各理想正答率のずれはa_j+m_j以下 | (K2)。同じCPTP写像・効果ノルム/距離の定義が必要 |
| CAL-03 | 補正下限L_calから理想基準のF_eを下から評価できる | (K3)、名目基底の相補性、前回の同時被覆 |
| CAL-04 | 理想入力の分枝下限はℓ_b−a_*を零切りする | (K4)。r_ideal=0は保留、零確率の認定ではない |
| CAL-05 | 実際入力から名目目標への距離は別の式で上から評価する | (K5)。前回の理想入力の対象と交換しない |
| CAL-06 | 校正上限を決定論的に仮定すれば前回の同時被覆を保つ | §2。校正失敗予算・IIDの実証・任意停止は含まない |
| CAL-07 | 24構成カウントと3対象準備例を全て保存・検算した | §3、再現コード。実測カウントや最小ショット数ではない |
| CAL-08 | カウントを増やしてもこの保証式の校正予算の床は残る | (K6)。真の物理誤差や全手法の最適下限ではない |
| CAL-09 | 未校正で全五記録が一致しても理想F_eと出力距離は異なり得る | §4のI/Z対照。共通座標ゲージではなく相補性の損失 |
| CAL-10 | 8行列ケース・35高精度比較・旧統計監査を実行した | §5。試作の失敗と補正も記録。一般保証は解析が根拠 |
| CAL-11 | 記録の頻度、記録校正、予測安定性は別に根拠が必要 | §2–4。今回、観測者間の同一事実を認定していない |
| CAL-12 | 一課題を仮定付きの保証と識別限界の解析として完了 | 実機認定・一事実の現実化・存在論的becomingは未認定 |

全体履歴を表現できることと、内部に記録が形成されることの有限モデルでの両立は既存R4/R5の成果である。本補足は、その記録から理想基準の安定した予測を導く際に、統計・校正・入力/分枝の適用対象が別々に必要になることを定量化した。全体表現、内部記録、観測者間の一致、許容操作への予測安定性、単一事実の現実化、存在論的becomingを同一視しない。識別不能という結果から、特定の時間存在論の正しさも導かない。

**次の判断:** 総括と補足のレビュー・統合。物理的な適用を選ぶなら、対象ρ/b・要求τ/αに対し、(K1)の予算とIIDにどの独立した実際の証拠を与えられるかを先に決める。今回の小さい仮定予算や構成カウントを、その校正実証の代わりに使わない。
