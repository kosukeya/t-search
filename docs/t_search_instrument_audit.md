# 分枝操作の同定 — 非選択チャネルと分枝確率では足りない情報

2026-10-30、instrument-v1。[実施仕様](t_search_instrument_audit_protocol.md)の一課題を完了した。基点は 622dda6fda2cdcc60cef0f8fe876328a2dfdc67a。mainはR5cまで、R5dと二つの後続監査は未マージ[PR #24](https://github.com/kosukeya/t-search/pull/24)で継続する。旧R3/R5の証拠と結論は保持する。

**結論:** 一般には、非選択チャネルを完全に知り、全入力に対する分枝確率まで知っても、条件付き量子操作は決まらない。今回の候補対では各分枝確率が常に1/2でも、＋入力の条件付き状態の距離は1/√2となる。フラグと出力量子系の**同時確率**を追加すれば両候補を識別できる。これは標準の量子操作の区別をt-searchへ適用した解析であり、新しい同定不能定理や物理法則の発見とは扱わない。

## 1. 何が前回から増えたか

[R3総括 §2–4](t_search_r3_synthesis.md)は、限られた測定の不定性、同じ合成チャネルの内部実装の不定性、八つの信頼条件を既に区別した。[条件付き予測監査 §2–5](t_search_conditioning_audit.md)は、同じCP分枝を二つの入力状態へ作用させる上限を導いた。

今回は「既知としている装置」をこの二系列へ照合する。**同じ入力に対する二つの候補装置**を比べ、非選択出力とフラグ周辺分布が同じでも、フラグ付き出力が異なるかを検査する。R3の内部方式の相違を再発見として数えず、窓口にフラグを含めることが何を追加するかを明示する。前回の「同じ装置」の条件を無断で変更した実験ではない。

LはR5のQ支持 {|000⟩,|110⟩}の論理量子ビット。Q内で復号してLを取り出せるが、復号はF1記録を消す。新しいフラグBは元のF1のZ記録ではない。E非アクセス、信頼準備・測定、固定次元、同一装置・リセット・設定漏れなし・全結果保持・厳密なBorn確率を仮定する。

## 2. 同じチャネル・同じ分枝確率の解析対照

$U_\alpha=e^{i\alpha Z}$、$0\le\alpha<\pi$ として

$$
K_0^{(\alpha)}=U_\alpha/\sqrt2,\quad
K_1^{(\alpha)}=ZU_\alpha/\sqrt2,\quad
\Phi_b^{(\alpha)}(A)=K_b^{(\alpha)}A K_b^{(\alpha)\dagger}.
$$

各分枝はCPで、$K_b^\dagger K_b=I/2$。従って和はTPであり、**任意の正規化入力の分枝確率は1/2**。任意の入力演算子Aについて

$$
\Lambda_\alpha(A)=\sum_b\Phi_b^{(\alpha)}(A)
=U_\alpha\frac{A+ZAZ}{2}U_\alpha^\dagger
=\Delta_Z(A). \tag{I1}
$$

最後の等号は対角演算子と$U_\alpha$が可換なため。全4行列単位で成立するので、参照を加えた非選択チャネル検査でもαを識別できない。さらにフラグ確率を全入力で知っても、全て1/2である。

同じ写像のKraus表現の関係は
$(K_0^{(\alpha)},K_1^{(\alpha)})^T
=\begin{pmatrix}\cos\alpha&i\sin\alpha\\i\sin\alpha&\cos\alpha\end{pmatrix}
(K_0^{(0)},K_1^{(0)})^T$。
この行列はユニタリ。非選択チャネルとしての等価性と、各Kraus項を公開フラグbへ対応させた量子操作の等価性は異なる。ラベルbは両候補で固定する。主候補α=0,π/4は、分枝の単なる位相倍やラベル交換でも同じ操作にならない。

Q全空間への拡張も可能である。$V|0⟩=|000⟩$、$V|1⟩=|110⟩$、$P=VV^\dagger$ とし、

$$
\widetilde K_b=V K_b V^\dagger+(I_Q-P)/\sqrt2.
$$

支持が直交するため $\widetilde K_b^\dagger\widetilde K_b=I_Q/2$。従って論理支持上だけの未定義な操作ではなく、Q全空間で完備な操作に延長できる。作用はQ内に閉じ、G上ではEの恒等とのテンソル積。支持外で非選択写像がF1デフェージングと等しいとは主張しない。

### R3の認定が返すもの

非選択出力を使うR3の四正答確率は両候補で (z0,z1,x_plus,x_minus)=(1,1,1/2,1/2)。既存[認定器](../src/t_search/r3_certificate.py)へこの解析上の厳密値と八条件の宣言を渡すと、$F_Z=1,F_X=1/2,[L,U]=[1/2,1/2]$。正規化Choi状態のBell重なりも $F_e=1/2$ である。

従ってR3の保証は正しく、性能区間が点になっても分枝写像を決めない。一般のチャネル同定に不足する四確率、完全に同じ非選択チャネル、装置の内部実装、という三つの不定性を混ぜない。フラグを含む出力は4次元であり、元の量子ビット→量子ビット認定器へそのまま渡せる新入力でもない。

## 3. 条件付き状態と、実際に分かれる全結果予測

$\rho_+=|+⟩⟨+|$ の入力で、両候補の正確率分枝を正規化すると次のようになる。$|\pm y⟩=(|0⟩\pm i|1⟩)/\sqrt2$。

| α | b=0の状態 | b=1の状態 | 非選択状態 | 分枝確率 |
| --- | --- | --- | --- | --- |
| 0 | ＋ | − | I/2 | 各1/2 |
| π/4 | −y | ＋y | I/2 | 各1/2 |

対応する二分枝の状態距離はともに $1/\sqrt2$。フラグ付き写像を
$\mathcal F_\alpha(A)=\sum_b|b⟩⟨b|_B\otimes\Phi_b^{(\alpha)}(A)$
とすれば、直和のトレースノルムから

$$
D(\mathcal F_0(\rho_+),\mathcal F_{\pi/4}(\rho_+))=1/\sqrt2. \tag{I2}
$$

一方、量子出力だけの距離も、フラグ周辺分布だけの距離も零。**両周辺分布が同じであることは、相関を含めた同時状態が同じことを意味しない。** この差は小確率の選別に由来しない。

フラグを保存し、両候補へ同じX測定を行う。順序を (0,+),(0,−),(1,+),(1,−) とすると

$$
P_0=(1/2,0,0,1/2),\qquad
P_{\pi/4}=(1/4,1/4,1/4,1/4),\qquad
\operatorname{TV}(P_0,P_{\pi/4})=1/2. \tag{I3}
$$

全分枝・全測定結果を保持する。等事前確率でこの一回の測定から最適に推測する成功率は3/4で、確実識別ではない。この測定の差1/2と、フラグ付き量子状態距離1/√2も区別する。単発で装置認定が完了したという主張ではない。

## 4. 何を追加すれば足りるか、どこまで足りないか

### 宣言した候補族だけなら

＋入力についてフラグとX/Y測定の同時確率から

$$
\chi_X=\sum_{b,x=\pm1}(-1)^b x\,P(b,x|+)=\cos(2\alpha),\quad
\chi_Y=\sum_{b,y=\pm1}(-1)^b y\,P(b,y|+)=-\sin(2\alpha). \tag{I4}
$$

X設定一つが主候補0/π/4の予測を分ける。X/Y二設定の厳密確率なら、この族のαをπを法として決められる。Xだけでは一般に位相の符号が決まらない。これは**族の形を既に仮定した**同定であり、任意の未知分枝写像を二つの数で認定する手順ではない。

### 一般の量子ビット分枝写像なら、十分な窓口を明示できる

信頼する四入力 $\rho_0,\rho_1,\rho_+,\rho_{+y}$ は演算子空間を張る。各入力jに対し、各bと出力X/Y/Zの**未正規化の同時確率** $P(b,\pm t|j)$ を保存する。$r_{bj}$を分枝確率、$v_{bjt}=P(b,+t|j)-P(b,-t|j)$ とすれば

$$
A_{bj}=\Phi_b(\rho_j)=\frac{r_{bj}I+\sum_{t=X,Y,Z}v_{bjt}t}{2}. \tag{I5}
$$

$A_0,A_1,A_+,A_y$ が分かれば、分枝ごとに
$\Phi_b(X)=2A_+-A_0-A_1$、
$\Phi_b(Y)=2A_y-A_0-A_1$、
$\Phi_b(|0⟩⟨1|)=(\Phi_b(X)+i\Phi_b(Y))/2$
と、対角成分・逆の非対角成分を再構成できる。よって四入力×三出力基底の12設定は、厳密確率・固定量子ビット空間で任意の線形分枝写像を決める十分なデータである。最小設定数は主張しない。

条件付き正規化済み状態だけを保存するとrを失う。ここでは損失・失敗・零分枝も未正規化データに含める。零分枝へ条件付き状態は割り当てない。有限標本でCP/TPと誤差を保証する推定器、SPAM補正、漏れやE非接続の物理監査は実施していない。完全なフラグ付き入出力写像が分かっても、その写像を実現する内部回路までは一意にならないというR3の限界も残る。

### 否定的結論を広げすぎない：厳密なユニタリの場合

非選択チャネルが厳密にユニタリ $\mathcal U$ と分かっている場合は例外である。正規化Choi演算子は階数1。分枝の正半定値Choi演算子の和がこの階数1演算子なら、各分枝は同じ一次元支持上にあり、$J_b=q_bJ_{\mathcal U}$。従って $\Phi_b=q_b\mathcal U$、分枝確率は入力によらずq_bで、正確率条件付き出力は全て $\mathcal U(\rho)$ と決まる。

R3で厳密な四正答率1から恒等チャネルと決まる極限もこの場合。今回のΔ_Z反例を「どの性能値でも絶対に分枝が決まらない」とは一般化しない。有限標本での近似ユニタリと稀な分枝に対する頑健な認定は本監査の範囲外。

## 5. 前回の保証と装置の仮定を照合する

| 使いたい結論 | 必要な対象・根拠 | 今回の否定的結果で失われるか |
| --- | --- | --- |
| R3の実行済み非選択チャネルの性能区間 | 四確率と八つの信頼条件 | 失われない。元々分枝写像を認定していない |
| 前回(C1)の入力状態対の条件付き上限 | 同じ完備な操作、入力差ε、分枝確率r,s>0 | 失われない。装置の個々のKraus行列を知る必要はない |
| 前回(C3)/(C4)の全分枝への十分上限 | 入力の相対的大小関係・κの根拠、Qに閉じる同じCP操作 | 失われない。任意の同じCP分枝に成立し、読出し位相の最適化も不要 |
| 前回の特定フィルターの等号やR5cの最大差達成 | 指定フィルター、既知p、適切な位相・読出しの作用 | 非選択データと分枝確率だけでその作用を逆算することはできない |
| 前回の元F1のLüders読出しによる厳密一致 | 指定した射影操作である根拠、確認したb | 単にbの頻度が合うだけでLüders操作と認定したことにはならない |
| 未知装置の配線・次元・校正・無選別 | 別の物理的根拠・全試行ログ等 | 今回も仮定。行列の一致で物理検証済みとはしない |

特に、フラグ距離零から前回(C1)の分子δF=0とは置けない。δFはフラグ**と量子出力**の距離であり、今回の両周辺分布の零差とは異なる。さらに(I2)は二つの装置同士の距離で、同じ装置に通したR5入力状態対のδFでもない。

## 6. 一次資料・検算・実行状態

2026-10-30に本文を確認した一次資料は次の二件。新規性の網羅的文献調査は行っていない。

| 一次資料 | 確認箇所と用途 |
| --- | --- |
| Watrous, [The Theory of Quantum Information](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf) | Corollary 2.23・式(2.99)–(2.100)のKraus表現、§2.3.2・式(2.258)–(2.262)の量子操作とフラグ付きチャネル、Proposition 2.44の情報完全性 |
| Hofmann, [Complementary classical fidelities…](https://arxiv.org/pdf/quant-ph/0409083) | 式(14)–(17)。R3の境界の対象を再確認し、分枝同定の境界へ読み替えない |

一般性の根拠は(I1)の全演算子上の恒等式、(I2)の直和ノルム、(I4)–(I5)の線形性、ユニタリ例外の正半定値支持の議論。有限検算だけで未知装置全体について結論していない。

| 実行した照合 | 結果 |
| --- | --- |
| α=0,π/8,π/4、全4入力行列単位 | 非選択Δ_Zとの12件の照合に成功 |
| フラグ効果・Q全空間への拡張 | 各入力確率1/2、Q上の6効果行列を照合 |
| 正規化Choi/BellとR3認定器 | 全候補F_e=1/2。厳密な四確率で区間[1/2,1/2] |
| 四入力×三基底×三候補 | 全36設定、144の生の同時確率を保持・規格化照合 |
| 同時確率からの分枝写像再構成 | 2分枝×4行列単位×3候補＝24件一致 |
| 主候補の条件付き距離・同時X分布 | 各0.7071067811865472、全結果TV=0.4999999999999998 |
| 最大解析・完備性・再構成残差 | 4.440892098500626e-16。絶対1e-10、相対0 |
| 実行環境 | Python 3.12.14 / NumPy 2.3.5 |

最初のパッケージ経由importは、この実行環境にnetworkxがなく失敗した。既存の標準ライブラリだけの認定器ファイルをrunpyで直接読み取り、下記の掲載コードで再実行して成功した。依存や認定器は変更していない。頻度データを作らず、R3へ渡す値は解析的な厳密確率で、行列からの値は独立照合にだけ使った。

文書検証では掲載コードを抽出して再実行し、同じ結果を確認した。変更した5文書の相対リンク105件、主張ID12件、表の列数、R3b/R5b/R5cのソースhash19項目・参照JSON hash2項目を照合し、git diff --checkも成功した。基点695追跡ファイル中692ファイルを保持し、変更は既存Markdown 3件と新規Markdown 2件だけ。README/roadmapの以前の本文と過去ログもそのまま保持した。

既存実装・テスト・JSONを変更しないため、全体pytestをローカルで繰り返していない。基点622dda6のpush [#40797100627](https://github.com/kosukeya/t-search/actions/runs/40797100627)は同SHAを検証し、1424テスト・18サブテスト成功（581.40秒）。PR [#40797104488](https://github.com/kosukeya/t-search/actions/runs/40797104488)はmainとのmerge ref 8ee99dee3f3bb3d62494487a356e981c741589c0を検証し、同数成功（750.60秒）。これは**基点**の結果。今回の文書headのCIはPRの最新検証欄で別記する。CIは以下の新しい解析を科学的に独立認定する仕組みではない。

### 実行可能な再現コード

リポジトリルートで、次のPythonコードを一時ファイルへ保存して実行する。NumPyだけを使い、既存認定器を読取り呼出しする。生成データや旧JSONへ書き込まない。コード中のQへの拡張は§2の支持外恒等の式で、数値上の分枝確率はクリップしない。

~~~python
import json, math, platform, runpy
import numpy as np
r3 = runpy.run_path('src/t_search/r3_certificate.py')
ASSUMPTION_KEYS, certify = r3['ASSUMPTION_KEYS'], r3['certify']
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
paulis = (X, Y, Z)
rhos = ((I+Z)/2, (I-Z)/2, (I+X)/2, (I+Y)/2)
units = [np.outer(I[:, i], I[:, j].conj()) for i in range(2) for j in range(2)]
assert np.linalg.matrix_rank(np.stack([r.reshape(-1) for r in rhos])) == 4
def branch(k, a): return k @ a @ k.conj().T
def distance(a, b): return float(np.linalg.svd(a-b, compute_uv=False).sum()/2)
def choi(action):
    return sum(np.kron(e, action(e)) for e in units)/2
bell = np.array([1, 0, 0, 1], complex)/math.sqrt(2)
errors, tables, conditional = [], [], []
counts = dict(operator_checks=0, reconstructed_operator_checks=0,
              joint_settings=0, joint_probabilities=0, embedded_effect_checks=0)
exact = dict(z0=1., z1=1., x_plus=.5, x_minus=.5)
certificate = certify(exact, {k: True for k in ASSUMPTION_KEYS})
assert certificate['lower_bound'] == certificate['upper_bound'] == .5
V = np.eye(8, dtype=complex)[:, [0, 6]]
complement = np.eye(8)-V@V.conj().T
for alpha in (0., math.pi/8, math.pi/4):
    U = math.cos(alpha)*I+1j*math.sin(alpha)*Z
    ks = (U/math.sqrt(2), Z@U/math.sqrt(2))
    channel = lambda a: sum(branch(k, a) for k in ks)
    for e in units:
        errors.append(float(np.max(np.abs(channel(e)-np.diag(np.diag(e))))))
        counts['operator_checks'] += 1
    for k in ks:
        errors.append(float(np.max(np.abs(k.conj().T@k-I/2))))
        kq = V@k@V.conj().T+complement/math.sqrt(2)
        errors.append(float(np.max(np.abs(kq.conj().T@kq-np.eye(8)/2))))
        counts['embedded_effect_checks'] += 1
    cj = choi(channel)
    errors.extend([abs(float(np.vdot(bell, cj@bell).real)-.5),
                   max(0., -float(np.linalg.eigvalsh(cj).min()))])
    probes = (rhos[0], rhos[1], rhos[2], (I-X)/2)
    for rho, key in zip(probes, exact):
        errors.append(abs(float(np.trace(rho@channel(rho)).real)-exact[key]))
    data = np.empty((4, 3, 2, 2))
    for j, rho in enumerate(rhos):
        for t, P in enumerate(paulis):
            for b, k in enumerate(ks):
                for m, sign in enumerate((1, -1)):
                    data[j, t, b, m] = np.trace((I+sign*P)/2@branch(k, rho)).real
            assert data[j, t].min() >= -1e-10
            errors.append(abs(float(data[j, t].sum())-1))
            counts['joint_settings'] += 1
            counts['joint_probabilities'] += 4
    for b, k in enumerate(ks):
        outputs = []
        for j in range(4):
            mass = float(data[j, 2, b].sum())
            v = data[j, :, b, 0]-data[j, :, b, 1]
            outputs.append((mass*I+sum(v[t]*P for t, P in enumerate(paulis)))/2)
        a0, a1, ax, ay = outputs
        bx, by = 2*ax-a0-a1, 2*ay-a0-a1
        recovered = (a0, (bx+1j*by)/2, (bx-1j*by)/2, a1)
        for e, rec in zip(units, recovered):
            errors.append(float(np.max(np.abs(rec-branch(k, e)))))
            counts['reconstructed_operator_checks'] += 1
    chi = [float(np.sum(data[2, t]*np.array([[1, -1], [-1, 1]]))) for t in (0, 1)]
    errors.extend([abs(chi[0]-math.cos(2*alpha)), abs(chi[1]+math.sin(2*alpha))])
    tables.append(data[2, 0].reshape(-1))
    conditional.append([2*branch(k, rhos[2]) for k in ks])
d = [distance(a, b) for a, b in zip(conditional[0], conditional[2])]
errors.extend(abs(v-1/math.sqrt(2)) for v in d)
tv = float(np.abs(tables[0]-tables[2]).sum()/2)
errors.append(abs(tv-.5))
assert max(errors) <= 1e-10
print(json.dumps(dict(python=platform.python_version(), numpy=np.__version__, **counts,
    max_residual=max(errors), conditional_distances=d, flagged_distance=sum(d)/2,
    joint_x_tv=tv, joint_x_alpha0=tables[0].tolist(), joint_x_alpha_pi4=tables[2].tolist(),
    r3_interval=[certificate['lower_bound'], certificate['upper_bound']]), indent=2))
~~~

## 7. 主張台帳・含意・次の判断

| ID | 主張 | 根拠と限界 |
| --- | --- | --- |
| INS-01 | 全候補の非選択チャネルはΔ_Z | (I1)、全演算子の証明。参照付き非選択検査でも同じ |
| INS-02 | 全入力の分枝確率は各1/2 | K†K=I/2。Q全空間へ完備に拡張、Eアクセスなし |
| INS-03 | 同じチャネルと全分枝確率でも分枝写像は一般に決まらない | 主候補0/π/4、§3。小確率選別を使わない |
| INS-04 | R3の性能区間は同じ[1/2,1/2] | 厳密四確率、既存認定器、独立Choi。元の認定の失敗ではない |
| INS-05 | 両周辺分布が同じでも同時出力は異なる | (I2)。フラグ付き状態距離1/√2 |
| INS-06 | 同じフラグ＋X測定で両候補の予測が分かれる | (I3)、全4結果TV=1/2。確実識別ではない |
| INS-07 | X/Y相関は宣言候補族の位相を決める | (I4)、αをπを法として同定。一般装置認定ではない |
| INS-08 | 四入力×三基底の同時確率は量子ビット分枝写像の再構成に十分 | (I5)、線形な全4行列単位の復元。厳密確率・信頼基準・固定次元 |
| INS-09 | 厳密なユニタリ非選択チャネルは例外 | §4の階数1 Choi支持。近似・有限標本の頑健性は未実施 |
| INS-10 | 同じ未知CP操作に対する前回の上限は保持される | §5。同定不能と、全操作に一様な上限を混同しない |
| INS-11 | 装置・窓口の同定と存在論的更新は別 | §1・下段。Bは元の記録値でなく、単一事実・主体間同定は未認定 |
| INS-12 | 一課題を解析・既存認定器照合として完了 | §6。新認定器、実機検証、有限標本保証、文献上の新規性は主張しない |

blockness／becomingへの追加理解は、全結果を表す記述と、内部で確認したフラグに基づく予測を結ぶために、周辺データに加えて操作と出力の相関を指定する必要があるという点である。非選択状態やフラグ頻度だけを「現在の記録が与える全情報」と扱わない。

ただし、これは出力の窓口の違いを調べた監査であり、新たな全体制約履歴や物理時計の実装を構成した成果ではない。内部の記録形成、観測者間の一致、許容操作への予測安定性、一つの事実の現実化、存在論的becomingを区別する。フラグが一つ実際に得られたという情報は条件付けの入力であり、その現実化の機構を本計算から導かない。全体履歴を表せることや操作同定から、未来の等しい実在／非実在も選ばない。

**次の判断:** 総括・条件付き保証・今回の窓口監査をレビューして統合する。追加の研究を行うなら、一般の装置認定へ広げる前に、どの具体的な条件付き予測にどの校正誤差を許す必要があるかを決める。今回の12設定の十分性を、そのまま有限標本・未知SPAMの実機認定済みとは扱わない。R3/R5の閉じた再現課題や旧Stageの判断は変更しない。

