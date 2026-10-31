# R3認定からの条件付き予測誤差 — 分枝同定なしで使える十分上限

2026-10-31、branch-bound-v1。[実施仕様](t_search_branch_bound_protocol.md)の一課題を完了した。基点は 5689496279c4c2519bf459fc26a068e838006e7a。mainはR5cまでで、R5dと後続補足は未マージ[PR #24](https://github.com/kosukeya/t-search/pull/24)にある。同じ研究ブランチを継続し、旧報告・仕様・台帳・実装・保存JSONは保持する。

**結論:** 量子ビットの非選択チャネルの恒等目標への忠実度下限Lと、対象入力での分枝確率p_b>0が正当化されていれば、分枝行列の同定なしで、理想出力ρとの条件付き距離に
$d_b(\rho)\le\min(1,\sqrt{2(1-L)/p_b(\rho)})$
という十分上限を使える。最良定数とは主張しない。分枝確率を除いた保証ではなく、近い非選択チャネルから全ての稀な分枝の小誤差を導くこともできない。

## 1. 問い・比較対象・前回との関係

[前回の分枝同定監査 §4](t_search_instrument_audit.md)では、非選択チャネルが厳密にユニタリなら正確率条件付き出力も決まると示した。その近傍で必要な誤差保証を一つ選ぶ。[R3](t_search_r3_synthesis.md)の性能下限を、そのまま分枝同定や最悪入力誤差と呼ぶのではなく、以下の補題と分枝確率の根拠を追加する。

対象は固定した量子ビット入力→量子ビット出力のCPTP写像 $\Lambda=\sum_b\Phi_b$。各分枝Φ_bはCP、全分枝を足すとTP。理想目標は恒等チャネル。比較するのは

$$
p_b(\rho)=\operatorname{Tr}\Phi_b(\rho)>0,\quad
\rho_{|b}=\Phi_b(\rho)/p_b(\rho),\quad
d_b(\rho)=D(\rho_{|b},\rho),\quad
D(A,B)=\tfrac12\|A-B\|_1.
$$

以前の[R5条件付き監査](t_search_conditioning_audit.md)が扱った「同じ操作に通す二つの入力状態」と異なり、今回は「同じ入力の実際の回復出力と理想回復出力」を比較する。元のF1記録のLüders読出しとも別で、bは回復操作の公開フラグである。新しい全体履歴・物理時計・装置実装を構成した研究ではない。

R3の八条件と、対象となるフラグ付き処理・確率の適用対象を固定する。準備・測定、次元、配線、リセット、設定漏れや試行選別の不在は依然として仮定。装置はEや参照を操作する資源を与えられていないと仮定するが、出力忠実度からその配線を認定するわけではない。厳密なBorn確率を扱い、有限標本とSPAM補正は含めない。

## 2. 一般上限の導出

分枝ごとのKraus演算子を $K_{b\mu}$ とする。μは公開しない分枝内の添字でもよい。次の分解を使う。

$$
K_{b\mu}=a_{b\mu}I+B_{b\mu},\qquad
a_{b\mu}=\tfrac12\operatorname{Tr}K_{b\mu},\qquad
\operatorname{Tr}B_{b\mu}=0.
$$

正規化Bell状態 $|\Omega⟩=(|00⟩+|11⟩)/\sqrt2$ に対する過程忠実度を、R3と同じ**平方根を取らない重なり**で定義する。$⟨\Omega|(I\otimes K)|\Omega⟩=\operatorname{Tr}K/2$ とTP条件から

$$
F_e=\sum_{b,\mu}|a_{b\mu}|^2,\qquad
\eta:=1-F_e=\tfrac12\sum_{b,\mu}\|B_{b\mu}\|_{\rm HS}^2. \tag{B1}
$$

R3の四つの非選択正答確率から得る
$L=\max(0,F_Z+F_X-1)\le F_e$
を使えば、$\eta\le e:=1-L$。eは過程忠実度欠損の上限で、R5の状態対のTV許容値εではない。

ρの任意の純化を $|\psi⟩_{RS}$ とし、装置はSだけへ作用する。$A_b=(\mathrm{id}_R\otimes\Phi_b)(|\psi⟩⟨\psi|)$、$p_b=\operatorname{Tr}A_b$。理想純化に直交する出力重みを $w_b=\operatorname{Tr}[(I-|\psi⟩⟨\psi|)A_b]$ とすると、恒等成分aは直交射影で消えるので

$$
\begin{aligned}
w_b
&=\sum_\mu\|(I-|\psi⟩⟨\psi|)(I_R\otimes B_{b\mu})|\psi⟩\|^2\\
&\le\sum_\mu\|B_{b\mu}\|_{\rm op}^2
\le\sum_\mu\|B_{b\mu}\|_{\rm HS}^2
\le 2\eta\le 2e. \tag{B2}
\end{aligned}
$$

純粋状態との距離には
$D(\sigma,|\psi⟩⟨\psi|)\le\sqrt{1-⟨\psi|\sigma|\psi⟩}$
が成り立つ。純粋なσでの二固有値計算と、混合へのトレースノルム凸性・Cauchy–Schwarzからも導ける。$\sigma=A_b/p_b$ に代入し、参照を捨てても距離は増えないことを使うと

$$
\boxed{
D(\Phi_b(\rho)/p_b,\rho)
\le D(A_b/p_b,|\psi⟩⟨\psi|)
\le\min\!\left(1,\sqrt{\frac{2(1-L)}{p_b(\rho)}}\right).
} \tag{B3}
$$

任意入力・任意の完備な分枝への解析であり、各Kraus行列を検証者が知る必要はない。参照Rは証明と独立照合側だけの資源で、R5の観測者に相関参照を使わせる新実験ではない。条件付き正規化は入力依存で非線形になり得るので、(B3)を二つのCPTPチャネルのdiamond距離と呼ばない。

L=1では全Bが零となり、各分枝は入力によらない確率で恒等目標を実行する。前回の厳密ユニタリ例外と整合する。零確率分枝の状態は定義しない。

## 3. 具体的な予測誤差の予算と追加証拠

対象入力で $p_b(\rho)\ge r_0>0$ が正当化されれば、同じ決定論的後処理と全結果を保持する任意の測定についても、条件付き予測のTV差は $\min(1,\sqrt{2e/r_0})$ 以下。さらに後続結果で選別・再条件付けする場合は、その確率も別途必要になる。

誤差τ以内を要求するなら、**この十分上限による一つの採用条件**は $e\le r_0\tau^2/2$。必要条件や最良の設計とはしない。

| 忠実度欠損上限e | 正当化した分枝確率下限r₀ | 十分な条件付きTV上限 |
| --- | ---: | ---: |
| 10^-4 | 0.1 | 約0.0447214 |
| 10^-6 | 0.01 | 約0.0141421 |
| 10^-6 | 0.02 | 0.01 |
| 10^-6 | 10^-6 | 1（非自明な保証なし） |

四正答確率だけから未知のp_bを認定した成果ではない。p_bは**その入力での**分枝確率であり、最大混合入力などで平均した頻度を無断で代用しない。全入力への一様な上限が必要なら、全対象入力で成り立つr₀の根拠が要る。未知入力の記述を装置へ知らせて処理を変える必要はないが、検証者がr₀をどう正当化するかは別の校正課題である。

R3の既存認定器は変更していない。その出力にこの条件付き上限が元から実装されていたとせず、本報告の解析としてLと外部のr₀をつなぐ。単なる分枝同定不能を理由に、今回の十分保証まで不能とは結論しない。

## 4. 負の結果と上限の限界

### 稀な誤動作分枝と平方根依存

未知入力に依存しない完備な論理操作

$$
K_0=\sqrt{1-q}I,\qquad K_1=\sqrt q\,e^{i\alpha Z}
$$

を考える。0≤q≤1、分枝1はq>0で条件付ける。四正答確率は
$(1,1,1-q\sin^2\alpha,1-q\sin^2\alpha)$、
従って $L=F_e=1-q\sin^2\alpha$。＋入力では

$$
p_1=q,\qquad d_1=|\sin\alpha|
=\sqrt{\frac{1-F_e}{q}}. \tag{B4}
$$

- α=π/2、q→0なら非選択チャネルは恒等へ近付くが、分枝1の出力は−で、＋との距離1が残る。q=0の分枝は零確率であり、厳密恒等の場合の例外に矛盾しない。
- q=1、α→0なら確率1の出力でも $d=\sqrt{1-F_e}$。一般に忠実度欠損と同じ一次の誤差を主張できず、平方根の尺度が必要になる。
- 例えば同じ四確率 $(1,1,1-e,1-e)$ を、q=e・α=π/2でも、q=1・$\alpha=\arcsin\sqrt e$でも得る。分枝確率の追加根拠を四確率だけで置き換えられない。この比較は解析で、検査ごとに同じ未知装置を取り替える指示ではない。

| q | α | L=F_e（解析） | ＋入力の分枝1距離 |
| --- | --- | ---: | ---: |
| 1 | π/12 | 約0.9330127019 | 約0.2588190451 |
| 10^-2 | π/12 | 約0.9993301270 | 約0.2588190451 |
| 10^-6 | π/12 | 約0.9999999330 | 約0.2588190451 |
| 10^-6 | π/2 | 0.999999 | 1 |

最後の例でフラグ＋Xの全結果を残すと、順序 (0,+),(0,−),(1,+),(1,−) で実際の分布は (1−q,0,0,q)。同じフラグ確率の理想恒等対照は (1−q,0,q,0)、全結果TVはq。全体の小誤差と、稀な分枝の誤差1は両立する。以前の「入力の偏りと同じフィルター」の例とは異なり、今回は固定した＋入力と、回復装置の誤動作分枝の関係である。

### 非ユニタル・複数Krausの対照

振幅減衰
$K_0=\operatorname{diag}(1,\sqrt{1-q})$、
$K_1=\sqrt q\,|0⟩⟨1|$
でも(B1)–(B3)を照合した。二分枝公開と、一つの分枝に二Krausをまとめる場合の両方を使う。後者は全結果を足す粗視化で、失敗試行を捨てた選別ではない。

ここでは $F_Z=1-q/2$、$F_X=(1+\sqrt{1-q})/2$、
$F_e=(1+\sqrt{1-q})^2/4$ で、一般にLとF_eは一致しない。分枝1の確率は $q\rho_{11}$ と入力に依存する。ユニタリ分枝・一定確率・L=真値だけを仮定して上限を検査していない。

(B3)の定数2の最適性は未検証である。例えば実測されたLが低く、上限1しか返せないことは認定保留であり、その入力や他の回復器で回復不能という結論ではない。

## 5. 一次資料、実行と未実施の検証

2026-10-31に一次本文の指定箇所を確認した。以下の既知原理を規約をそろえて適用し、(B1)–(B3)を導出した。これらの資料がこの分枝上限そのものを述べたという引用ではない。新規性の網羅的監査も行っていない。

| 一次資料 | 確認箇所・用途 |
| --- | --- |
| Hofmann, [Complementary classical fidelities…](https://arxiv.org/pdf/quant-ph/0409083) | 式(14)–(17)。R3の非選択チャネルの忠実度下限 |
| Fuchs–van de Graaf, [Cryptographic Distinguishability Measures for Quantum Mechanical States](https://arxiv.org/pdf/quant-ph/9712042) | Theorem 1、式(46)と証明。状態距離とroot fidelityの規約。純粋目標ならその二乗は本報告の重なり |
| Watrous, [The Theory of Quantum Information](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf) | Theorem 2.22、Theorem 3.33、Corollary 3.40/式(3.241)。CP表現と距離縮小の著者による本文 |

有限検算は[仕様](t_search_branch_bound_protocol.md)で固定した17操作。6入力の純化は0,1,＋,＋i,I/2と、非対称混合状態の純化
$\sqrt{0.7}|00⟩+\sqrt{0.3}|1⟩\otimes(\cos(\pi/3)|0⟩+e^{i\pi/5}\sin(\pi/3)|1⟩)$。
装置は参照を操作せず、純化を保持した距離と縮約出力の距離の両方を計算した。一般性は(B1)–(B3)の証明が根拠であり、有限点からの一般化ではない。

| 実行済みの検証 | 実測結果 |
| --- | --- |
| 17操作×全4入力演算子 | 68件、独立な解析写像と一致 |
| 全Kraus完備性・Choi/Bell・トレース零分解 | 解析真値・既存R3境界と照合 |
| 6入力の全分枝 | 正確率152件を照合、解析上零の28件は正規化せず保持 |
| 最大解析・完備性・規格化・射影恒等式残差 | 5.551115123125783e-16 |
| 最大の計算上の不等式超過 | 2.220446049250313e-16（丸め許容内。零へ書換えない） |
| 数値許容差・実行環境 | 絶対1e-10、相対0。Python 3.12.14 / NumPy 2.3.5 |

R3認定器には解析的な厳密四確率と八条件の宣言だけを渡し、行列・条件ID・参照真値は渡さない。行列から計算した四確率・Choi真値・全演算子は独立照合側に置いた。確率・固有値のクリップ、Born分布の選別、旧JSONの再生成を行わず、下記コードを実行して成功した。認定器は標準ライブラリだけのファイルをrunpyで読み、過去のpackage importの依存問題を持ち込んでいない。

文書から掲載コードを抽出して再実行し、同じ結果を確認した。変更した5文書の相対リンク111件、主張ID12件、表の列数、R3b/R5b/R5cのソースhash19項目・参照JSON hash2項目を照合。新規2文書の余分なEOF空行をstaged whitespace checkが検出したため修正し、再チェックした。基点697追跡ファイル中694を保持し、既存Markdown 3件への追記と新規Markdown 2件だけを変更した。README/roadmapの以前の本文と過去ログも保持した。

**未実施:** 実機の準備/測定/配線認定、未知SPAM・ドリフトの推定、有限標本からのL/r₀の同時信頼下限、新しい回復器や認定器、全体履歴・物理時計の実装。文書のみの変更なのでローカル全体pytestは反復せず、基点成功CIと新headのCIを区別する。

| 完了した基点CI | 実際のcheckout | 結果 |
| --- | --- | --- |
| [push #40981773943](https://github.com/kosukeya/t-search/actions/runs/40981773943) | 5689496279c4c2519bf459fc26a068e838006e7a | 1424テスト・18サブテスト、577.05秒、success |
| [PR #40981779204](https://github.com/kosukeya/t-search/actions/runs/40981779204) | mainとのmerge ref d440fadebaae509c4bbca90dac1841e5b6e5e6bf | 同数、583.37秒、success |

これは今回の文書追加前の回帰証拠。新headのCIは[PR #24](https://github.com/kosukeya/t-search/pull/24)の最新検証欄へ別記する。CIの回帰成功と、新しい解析の独立した科学的認定も同一ではない。

### 実行可能な再現コード

リポジトリルートで次のコードを一時Pythonファイルへ保存して実行する。NumPyと既存R3認定器だけを読み、旧データへ書き込まない。全17操作の計算値をJSONとして標準出力へ返す。零分枝は解析上の確率で特定し、微小な正確率を閾値で捨てない。

~~~python
import json, math, platform, runpy
import numpy as np
r3 = runpy.run_path('src/t_search/r3_certificate.py')
I = np.eye(2, dtype=complex)
Z = np.diag([1, -1]).astype(complex)
e0, e1 = I[:, 0], I[:, 1]
plus, minus = (e0+e1)/math.sqrt(2), (e0-e1)/math.sqrt(2)
plusi = (e0+1j*e1)/math.sqrt(2)
bell = np.array([1, 0, 0, 1], complex)/math.sqrt(2)
asym = math.sqrt(.7)*np.kron(e0, e0) + math.sqrt(.3)*np.kron(
    e1, math.cos(math.pi/3)*e0+np.exp(1j*math.pi/5)*math.sin(math.pi/3)*e1)
purifications = [np.kron(e0, v) for v in (e0, e1, plus, plusi)] + [bell, asym]
units = [np.outer(I[:, i], I[:, j].conj()) for i in range(2) for j in range(2)]
def dm(v): return np.outer(v, v.conj())
def reduce(a): return np.trace(a.reshape(2, 2, 2, 2), axis1=0, axis2=2)
def apply(ks, a): return sum(k@a@k.conj().T for k in ks)
def distance(a, b): return float(np.linalg.svd(a-b, compute_uv=False).sum()/2)
def rot_truth(a, q, alpha):
    t = (1-q)+q*np.exp(2j*alpha)
    return np.array([[a[0, 0], t*a[0, 1]], [t.conjugate()*a[1, 0], a[1, 1]]])
def ad_truth(a, q):
    s = math.sqrt(1-q)
    return np.array([[a[0, 0]+q*a[1, 1], s*a[0, 1]], [s*a[1, 0], (1-q)*a[1, 1]]])
cases = []
for q in (1., .01, 1e-6):
    for alpha in (0., math.pi/12, math.pi/2):
        u = math.cos(alpha)*I+1j*math.sin(alpha)*Z
        groups = [[math.sqrt(1-q)*I], [math.sqrt(q)*u]]
        f = 1-q*math.sin(alpha)**2
        cases.append(('rotation', q, alpha, groups, (1., 1., f, f), f))
for q in (0., .01, 1e-6, 1.):
    ks = [np.diag([1., math.sqrt(1-q)]).astype(complex), math.sqrt(q)*np.outer(e0, e1)]
    fx = (1+math.sqrt(1-q))/2
    f = (1+math.sqrt(1-q))**2/4
    for merged in (False, True):
        groups = [ks] if merged else [[k] for k in ks]
        cases.append(('ad_merged' if merged else 'ad_resolved', q, 0., groups, (1., 1-q, fx, fx), f))
errors, excesses, rows = [], [], []
positive = zero = operator_checks = 0
for family, q, alpha, groups, exact, expected_fe in cases:
    ks = [k for g in groups for k in g]
    errors.append(float(np.max(np.abs(sum(k.conj().T@k for k in ks)-I))))
    for a in units:
        truth = rot_truth(a, q, alpha) if family == 'rotation' else ad_truth(a, q)
        errors.append(float(np.max(np.abs(apply(ks, a)-truth))))
        operator_checks += 1
    cj = sum(np.kron(a, apply(ks, a)) for a in units)/2
    fe = float(np.vdot(bell, cj@bell).real)
    errors.extend([abs(fe-expected_fe), max(0., -float(np.linalg.eigvalsh(cj).min()))])
    bs = [k-np.trace(k)*I/2 for k in ks]
    eta = sum(float(np.trace(b.conj().T@b).real) for b in bs)/2
    errors.append(abs(eta-(1-fe)))
    data = dict(zip(('z0', 'z1', 'x_plus', 'x_minus'), exact))
    cert = r3['certify'](data, {k: True for k in r3['ASSUMPTION_KEYS']})
    L, U = cert['lower_bound'], cert['upper_bound']
    excesses.extend([max(0., L-fe), max(0., fe-U)])
    for v, target in zip((e0, e1, plus, minus), exact):
        errors.append(abs(float(np.vdot(v, apply(ks, dm(v))@v).real)-target))
    e = 1-L
    selected = None
    for j, psi in enumerate(purifications):
        tau, rho = dm(psi), reduce(dm(psi))
        errors.append(abs(float(np.trace(tau).real)-1))
        total_mass = 0.
        for b, group in enumerate(groups):
            joint = apply([np.kron(I, k) for k in group], tau)
            p = float(np.trace(joint).real)
            total_mass += p
            expected_p = ((1-q, q)[b] if family == 'rotation' else
                          1. if family == 'ad_merged' else (1-q*rho[1, 1].real, q*rho[1, 1].real)[b])
            errors.append(abs(p-expected_p))
            if expected_p == 0:
                zero += 1
                errors.append(float(np.linalg.norm(joint)))
                continue
            assert p > 0
            positive += 1
            cond = joint/p
            dj, ds = distance(cond, tau), distance(reduce(cond), rho)
            w = float(np.trace((np.eye(4)-tau)@joint).real)
            projection = np.eye(4)-tau
            projected = sum(float(np.linalg.norm(projection@np.kron(I, k-np.trace(k)*I/2)@psi)**2) for k in group)
            errors.append(abs(w-projected))
            bound = min(1., math.sqrt(2*e/p))
            excesses.extend([max(0., dj-bound), max(0., ds-dj), max(0., projected-2*eta)])
            if family == 'rotation' and b == 1 and j == 2:
                errors.append(abs(ds-abs(math.sin(alpha))))
                selected = ds
        errors.append(abs(total_mass-1))
    rows.append(dict(family=family, q=q, alpha_over_pi=alpha/math.pi, L=L, F_e=fe,
                     plus_branch1_distance=selected))
assert max(errors) <= 1e-10
assert max(excesses) <= 1e-10
print(json.dumps(dict(python=platform.python_version(), numpy=np.__version__, instruments=len(cases),
    inputs=len(purifications), operator_checks=operator_checks, positive_branches=positive,
    zero_branches_not_normalized=zero, max_residual=max(errors), max_inequality_excess=max(excesses),
    rows=rows), indent=2))
~~~

## 6. 主張台帳とblockness／becomingへの含意

| ID | 主張 | 根拠・限界 |
| --- | --- | --- |
| BND-01 | 非選択の忠実度欠損はトレース零Kraus成分の二乗和 | (B1)。固定量子ビット・恒等目標、平方根なしのBell重なり |
| BND-02 | 個々の分枝の純化に直交する出力重みは2(1−L)以下 | (B2)。任意のCP分枝、非公開Kraus添字も全て足す |
| BND-03 | 正確率分枝で条件付き距離の十分上限(B3)を使える | 証明と152正確率分枝。最良定数は未主張 |
| BND-04 | r₀の追加根拠があれば具体的な予測誤差予算に使える | §3。四確率だけで未知pを認定していない |
| BND-05 | 高い非選択忠実度でも稀な分枝の誤差1が残り得る | (B4)、α=π/2・q→0。全結果差はqで矛盾なし |
| BND-06 | 一般に過程忠実度欠損と同じ一次の出力誤差は保証できない | (B4)、q=1・α→0。平方根尺度の例 |
| BND-07 | 厳密L=1の正確率分枝は恒等目標を保つ | (B1)のB=0。前回の厳密ユニタリ例外と整合、零分枝は未定義 |
| BND-08 | 非ユニタル・入力依存確率・混合分枝も検算した | §4–5の振幅減衰、公開/粗視化対照。有限照合は一般証明の代用でない |
| BND-09 | 新しい上限は分枝写像や内部回路の同定ではない | §1–3、旧INS-03との両立。正規化後の非線形写像をCPTPとしない |
| BND-10 | 理想的な信頼条件と分枝確率の適用対象は依然必要 | §1・3・未実施欄。有限標本・未知SPAM・配線は未認定 |
| BND-11 | 全体の性能と内部の条件付き予測を定量的に分けられる | 上限と反例。記録校正・主体間の事実同定とは別 |
| BND-12 | 一課題を標準量子形式の解析・照合として完了 | 新規性・新物理法則・単一事実・存在論的becomingの認定ではない |

全体を非選択チャネルとして評価する情報と、内部で確認したフラグに条件付けて使う予測の情報を、eとpの別々の条件として結べた。分枝を完全に同定しなくても、条件付き予測の安定性を限定的に保証できる一方、全体の小誤差だけで内部の全フラグを安全に使えるとはしない。

ここで保証するのは、与えられた結果の後に使う予測誤差である。全体履歴の表現、内部の記録形成、観測者間の一致、許容操作への予測安定性、一つの事実の現実化、存在論的becomingを同一視しない。フラグbが実際に一つ得られたという情報は条件付けの入力であり、(B3)はその成立機構や未来の実在/非実在を選ばない。ActualityやPotentialityを忠実度や確率で再定義することもない。

**次の判断:** 総括と補足のレビュー・統合に加え、具体的に必要なτとp下限の対象入力を定める。理想確率での本論点はここで区切り、さらに進むならLとpの根拠にどの有限標本・校正誤差を含める必要があるかを先に固定する。今回その統計認定を実施したとはしない。
