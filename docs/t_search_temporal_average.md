# 時間変動する処理と有限記録 — 共通平均の保証、各時点・将来の限界

2026-11-03、temporal-average-v1。[実行前プロトコル](t_search_temporal_average_protocol.md)の一課題を完了した。基点は [9005f761ca592a5d4e6f74400688b135b28800f1](https://github.com/kosukeya/t-search/commit/9005f761ca592a5d4e6f74400688b135b28800f1)、同じresearch/r5d-synthesis・[Draft PR #24](https://github.com/kosukeya/t-search/pull/24)を継承。mainはR5c統合 [4a0f32d8fdd87f7daa6a3f0a9cac4c81b6fac5c2](https://github.com/kosukeya/t-search/commit/4a0f32d8fdd87f7daa6a3f0a9cac4c81b6fac5c2)のままで、前回以後の外部コミット・レビュー追加はない。

**結論:** 同分布は必須ではない。独立な時間変動と、五設定に共通の時間重みが正当化されるなら、前回と同じKL下限・校正補正を**平均インストゥルメント**に使える。しかし平均保証は個別時点や次の試行の保証ではない。共通時間重みや独立性まで外す代用も成立しない。本報告は既知原理の適用・識別限界の具体化であり、装置の時間安定性の実証や新しい確率定理ではない。

## 1. 選んだ問いと、どの仮定を変えたか

[有限カウント](t_search_finite_counts.md)と[校正予算](t_search_calibration_budget.md)は同じ処理・IIDを仮定した。今回の問いは、そのうち同分布を緩めたとき**何について**保証を出せるかである。「IIDを検証済み」と宣言することや、一般のメモリ装置へ保証を拡張することを目的としない。

事前固定したnブロックを考える。ブロックtの量子ビットインストゥルメントを{Φ_t,b}、非選択チャネルをΛ_t=Σ_bΦ_t,bとする。列は固定され、結果・現在の設定に適応しない。各ブロックで、四正答検査と指定入力ρの公開フラグbを、同じ処理に一回ずつ適用する。各設定のブロック間の二値スコアは独立。クロス設定の独立性は一般の合併則には不要だが、§4の全判定確率を計算する対照では五設定間も独立に固定した。

この窓口は前回の任意サイズ・分離バッチから変更している。理由は、五つの率を**一つの同じ平均処理**へ対応させるため。同じブロックの五使用に同じ処理が使え、リセットされることも仮定であり、順をランダム化すれば自動的に証明される条件ではない。

全体で固定した実際の準備σ_j・効果M̃_j、対象準備σは前回と同じ型とする。各ブロックで、名目ρ_j/M_jからの準備距離a_j・効果ノルム誤差m_j、対象ρからの準備距離a_*が成り立つと仮定する。独立校正、次元・配線・設定漏れ/試行選別なし等の信頼条件は保持。数値対照は校正予算ゼロであり、未知SPAMを認定していない。

定義する対象は

$$
\bar\Phi_b=\frac1n\sum_{t=1}^n\Phi_{t,b},\qquad
\bar\Lambda=\sum_b\bar\Phi_b=\frac1n\sum_t\Lambda_t . \tag{T1}
$$

固定した列なので、この凸平均は正当なCPインストゥルメント/CPTPチャネルになる。将来に同じ混合を物理的に再現できることは別の仮定。平均の対象期間・重みは観測前に定め、結果の良い時間だけを選ばない。

## 2. 独立・非同分布の平均へのKL下限

一設定でY_t∈{0,1}、Pr(Y_t=1)=p_t、K=ΣY_t、μ=(Σp_t)/nとする。独立性とlogの凹性より、λ>0で

$$
\mathbb E e^{\lambda K}
=\prod_t\{1+p_t(e^\lambda-1)\}
\le\{1+\mu(e^\lambda-1)\}^n . \tag{T2}
$$

従ってμ<x≤1について

$$
\Pr(K/n\ge x)\le \exp[-n\,{\rm kl}(x\Vert\mu)] . \tag{T3}
$$

μ<x<1では前回と同じ指数の最小化を使う。x=1はΠp_t≤μ^nであり、**一般に等号ではない**。μ=0/1は直接処理する。Kは通常二項分布ではなくPoisson-binomial分布だが、KL尾による上側評価は同じ形で使える。

前回の片側下限ℓ(k,n)は、k=0で0、k>0でkl(k/n∥ℓ)=log(1/β)/nを解く。k=nならβ^(1/n)。ℓ(K,n)>μとなる最小カウントの上側尾へ(T3)を適用すれば、Pr(ℓ(K,n)>μ)≤β。従って**数値関数を変更せず、下から評価する対象を固定母数から時間平均μへ変えられる**。

これはHoeffdingの独立・有界変数に対する既存結果の適用であり、二項分布だと偽って扱う主張ではない。サンプルサイズ・設定・分枝・対象期間は固定。任意停止、適応的メモリ、事後選択や繰返し全体への同時保証は含めない。

## 3. 平均量子処理への接続と条件付けの対象

五つの平均実測率にβ=α/5を配分し、α=0.05とする。四検査の平均実測率と、名目入力を平均チャネルへ入れた理想正答率の差は、各ブロックで前回(K2)を適用して平均すればa_j+m_j以下。従って同時被覆事象上で

$$
s_j=\max(0,\ell_j-a_j-m_j),\qquad
L_{\rm avg}=\max\!\left(0,\frac{\sum_js_j}{2}-1\right)
\le F_e(\bar\Lambda)
=\frac1n\sum_t F_e(\Lambda_t). \tag{T4}
$$

Hofmann下限は同じ名目相補基底に対する、同じ平均チャネルへ適用する。Bell重なりF_eの線形性を使っており、平均状態忠実度や「各時点の最小忠実度」と交換しない。

フラグ平均率はp̄_b(σ)=Tr Φ̄_b(σ)。名目入力の下限はr_avg=max(0,ℓ_b−a_*)。r_avg>0なら、[分枝上限](t_search_branch_bound.md)を平均インストゥルメントへ適用して

$$
D\!\left(\frac{\bar\Phi_b(\rho)}{\bar p_b(\rho)},\rho\right)
\le U_{\rm avg}
=\min\!\left(1,\sqrt{\frac{2(1-L_{\rm avg})}{r_{\rm avg}}}\right). \tag{T5}
$$

r_avg=0なら本手続きの理想入力の主張は保留。実際の固定準備σから名目ρまでの距離には、前回(K5)と同じmin(1,a_*+sqrt(2(1−L_avg)/ℓ_b))を、ℓ_b>0のとき使える。校正上限を決定論的に仮定した下で、これらの平均についての偽保証事象の無条件確率はα以下。校正上限自体の統計的失敗予算は今回も含めない。

p_t,b=Tr Φ_t,b(ρ)>0の時間別状態をρ_t,bとすると、

$$
\frac{\bar\Phi_b(\rho)}{\bar p_b(\rho)}
=\sum_{t:p_{t,b}>0}\frac{p_{t,b}}{\sum_s p_{s,b}}\,\rho_{t,b}. \tag{T6}
$$

**条件付き状態の等重み平均ではなく、分枝確率で重み直した平均**である。零分枝は正規化しない。時刻記録を明示するCQ表現の非正規化bブロックω_TbQ=(1/n)Σ_t|t⟩⟨t|⊗Φ_t,b(ρ)を用いる。tを周辺化して正規化したものが(T6)、tを知って条件付けたものがρ_t,bであり、同じ予測対象ではない。tは実験の古典的ラベルで、R5のコヒーレント履歴や宇宙の物理時計を実装したレジスタではない。

## 4. 有理数で全カウントを監査した結果

n=8,25,100、平均p=0.01,0.1,0.5,0.9,0.99で、一定列、p±min(p,1−p)/2の交互列（奇数末尾はp）、総和npを1・一つの端数・0へ集中した列を固定した。45列のPoisson-binomial分布をFractionの有理数DPで求め、全カウントの失敗確率Pr(ℓ(K)>p)を総和した。一定列の全分布は別の二項式計算と完全一致した。

| n | 平均p | 一定列 | 交互列 | 集中列 |
| --- | --- | --- | --- | --- |
| 8 | 1/100 | 0.00269007774 | 0.002601646326 | 0 |
| 8 | 1/10 | 0.00043165 | 0.0003040142578 | 0 |
| 8 | 1/2 | 0.00390625 | 0.001235961914 | 0 |
| 8 | 9/10 | 0 | 0 | 0 |
| 8 | 99/100 | 0 | 0 | 0 |
| 25 | 1/100 | 0.00195067689 | 0.001901430575 | 0 |
| 25 | 1/10 | 0.0004575492931 | 0.0003564113783 | 0 |
| 25 | 1/2 | 0.002038657665 | 0.0005260403598 | 0 |
| 25 | 9/10 | 0 | 0 | 0 |
| 25 | 99/100 | 0 | 0 | 0 |
| 100 | 1/100 | 0.000534534464 | 0.0005203484862 | 0 |
| 100 | 1/10 | 0.0008075738744 | 0.0006664440972 | 0 |
| 100 | 1/2 | 0.0008949651957 | 0.0001603620634 | 0 |
| 100 | 9/10 | 0.001944884652 | 0.001757275406 | 0 |
| 100 | 99/100 | 0 | 0 | 0 |

全45条件でβ=0.01以下、最大は一定列n=8・p=1/2の0.00390625。集中列の零はこの固定した支持上の結果であり、全ての非同分布列で失敗確率が零になる意味ではない。一般被覆の根拠は(T2)–(T3)と離散尾の解析である。

### 平均分枝についての全17,576判定

位相反転フラグΦ_t,0(ρ)=q_t ZρZ、Φ_t,1(ρ)=(1−q_t)ρを用い、対象は＋入力の分枝0。n=25、平均q=0.1を保つ三列を固定した。全てF_e(Λ̄)=0.9、p̄_0=0.1、条件付き距離1。独立な三つの非自明カウント（X二設定とフラグ）について26³=17,576判定を全て計算した。

| q_tの列 | 誤って1未満の条件付き上限を出す確率 |
| --- | --- |
| 0.1を25回 | 約1.1933852813e-25 |
| (0,0.2)を12組＋0.1 | 0 |
| 1,1,0.5と22個の0 | 0 |

各列の正確な分布の積を有理数で全和した。非自明上限を出すカウント組は全体で4個。この制御条件の結果を一般の失敗率・最適性へ拡張しない。物理ショットを実行した報告ではない。

## 5. 七つの量子処理列と、誤って移せない保証

七列×三入力（＋、0、(I+0.2X+0.3Y+0.4Z)/2）の21条件を検算した。時刻別I/ZのKraus行列を重み付きで連結した平均と、時刻別出力を直接平均する別の計算を比較。Bell状態によるF_eは、時刻別のKrausトレース式とも照合した。表は校正予算ゼロ・厳密確率での＋入力の値で、有限カウントの値とは別である。

| 処理列 | ブロック数 | F_e(Λ̄) | p̄_0 | 距離（＋） | (T5)上限 |
| --- | --- | --- | --- | --- | --- |
| 全て恒等I | 1 | 1 | 1 | 0 | 0 |
| 全てZ | 1 | 0 | 1 | 1 | 1 |
| I,Z | 2 | 0.5 | 1 | 0.5 | 1 |
| 誤り率0,0.02を同一フラグに粗視化 | 2 | 0.99 | 1 | 0.01 | 0.1414213562 |
| 同じ誤り率でZ分枝のフラグを保持 | 2 | 0.99 | 0.01 | 1 | 1 |
| 分枝重み0.25/0.75、作用I/Z | 2 | 0.625 | 0.5 | 0.75 | 1 |
| 999回I、最後だけZ | 1000 | 0.999 | 1 | 0.001 | 0.0447213595 |

0入力の距離は全て0。混合入力の距離は、各行の＋距離にsqrt(0.13)を掛けた値であり、独立行列計算と一致した。稀な分枝の第1時刻で零確率となる三入力の状態は正規化せず保持した。稀なZ分枝の例は既存の反例を時間列として具体化したもので、別の新しい物理効果とは数えない。

### 分枝条件付けの時間重み

第1時刻は分枝0が確率0.25でI、第2時刻は確率0.75でZ、残りの分枝はIとした対照では、分枝0の平均条件付き状態は0.25ρ＋0.75ZρZ。＋入力の距離は0.75。二つの時間別条件付き状態を等重みで平均すると距離0.5になり、異なる予測を返す。(T6)の重み直しが必要である。

### 平均保証を特定時点へ移せない

999回I・最後だけZは、本報告の独立・非同分布・共通時間重みの仮定内にある。＋入力の平均距離0.001に対して最後の距離は1。さらにこの列で得る構成カウントは、Z二設定が各1000/1000、X二設定が各999/1000、フラグが1000/1000。全て決定論的な結果であり、有限下限はL_avg≈0.9877923686、r_avg≈0.9954054174、U_avg≈0.1566140431を返す。

これは平均の0.001を上から評価するが、最後の1は上から評価しない。時刻tを新たに条件として使える操作クラスへ広げる際、平均証明をそのまま使ってはならない。[R5の条件付き予測監査](t_search_conditioning_audit.md)と同じく、条件に使う情報を指定する必要がある。

### 共通時間重みを外せない

検証したい対象を、固定した二つの時刻条件Z/Iの等重み平均とする。Z検査はZの時刻だけ、X検査はIの時刻だけで実施し、公開フラグは常に0とする。入力設定をチャネルへ渡して切り替える装置ではなく、事前固定した処理の時間列と、偏った設定スケジュールで構成できる。

五つの記録は全成功でも、四率は**異なる時間平均**を測っている。各バッチn=100の全成功を旧合成式へ入れるとL≈0.9099851720、U≈0.4341822108。しかし等重み平均のF_eは0.5、＋距離も0.5で、双方に誤った保証になる。これは(T4)–(T5)の反例ではなく、共通時間重みという適用条件を破る反例である。バッチ内の各列は完全に決定論的・独立でも、この欠落は残る。

### 次の試行と独立性にも別の仮定が要る

装置A/Bが検査期間中は全く同じ恒等処理、次だけAはI、BはZとなる固定した二つの列を考える。全ての過去の検査入力に対する量子出力と記録は一致し、n=100の全成功カウントも確率1で得られる。次の＋入力の距離は0/1。将来の変動を制約しない模型では、この同じ過去の記録から次の距離1を排除する非自明な普遍保証は出せない。

また独立性を外し、全Y_tが一つの共通Bernoulli(1/2)変数Cに等しい例では、各時刻の**無条件周辺確率**は1/2。n=100でℓ(100,100)≈0.9549925860>1/2となり、周辺平均に対する偽下限の確率は1/2でβ=0.01を超える。隠れたCに条件付けた別の母数の問題とは区別する。同分布を緩めた(T2)を、依存性や一般の適応的メモリへ無断で拡張できない。

## 6. 実行・一次資料・検証状態

Python 3.12.14、NumPy 2.3.5でプロトコルの全条件を実行した。21行列条件の155比較と21不等式を確認し、最大残差は4.45e-16未満、正の不等式超過は0。数値走査はI/Zの固定対照であり、任意のCPTP写像への一般性は解析が根拠である。生の行列計算で生じた1+2e-16程度の値を保存し、物理確率を都合よく修正して成功にはしていない。

前回の掲載コードを変更せず実行し、303有理数被覆・17,576判定/5真値・145高精度根を再確認した。今回追加で用いた999/1000の逆根も、独立の60桁Decimalで下向き余裕後の保守性を確認した。余裕前の差は0だった。掲載コードを抽出した再実行のJSON出力も完全一致した。数学的被覆と、宣言した数値例での丸めの照合を区別し、新しい汎用認定器は作っていない。

既存の文書整合性30ファイルの196 assertion関数を直接実行して成功した。pytest suiteの実行ではなく、他モジュール依存の3ファイルは対象外。このローカル環境にpytestはない。相対リンク129件、表13個、主張ID12件、ソースhash19項目・参照JSON hash2項目、基点703ファイル中700 blobと旧進捗本文の保持を確認した。変更は既存進捗Markdown 3件への追記と新規Markdown 2件だけで、削除はない。staged whitespaceも照合し、完全な回帰CIは下記の正確なheadで区別する。

2026-11-03に一次資料の次の本文箇所を確認した。

| 一次資料 | 確認箇所と用途 |
| --- | --- |
| Hoeffding, [Probability Inequalities for Sums of Bounded Random Variables](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf), JASA 58 (1963) | printed pp.14–15、式(1.7)–(1.9)、Theorem 1・式(2.1)と端点の説明をスキャン画像で実際に読んだ。条件は独立・有界で、同分布ではない。(T2)–(T3)の既知の根拠 |
| Hofmann, [Complementary classical fidelities…](https://arxiv.org/pdf/quant-ph/0409083) | 式(14)–(17)、特に(15)。同じ平均チャネルの相補基底率への下限 |

文献全体に対する新規性を確立した成果ではない。「同分布は不要」という既知結果自体を発見として数えず、t-searchで前二報の保証がどの平均に適用され、どこで使えなくなるかを監査した。

**実行済み:** 導出、45分布の全カウント、全17,576判定の三列での確率和、七処理列×三入力、時間重み・特定時点・将来・依存性の対照、既存統計コードと追加根の照合。今回の研究計算の最終チェックは全て成功した。

**未実施・保留:** 実機の独立性・リセット・ブロック内同一処理・共通時間重み・校正の認定、ドリフトの推定、適応的メモリ、任意停止・事後選択、将来処理の保証、物理時計・全体履歴・単一事実の実装。旧仕様・認定器のexact_probabilities契約・ソース・テスト・保存JSONは変更していない。文書だけなのでローカル全体pytestは反復していない。

基点push [#41370842427](https://github.com/kosukeya/t-search/actions/runs/41370842427)はcheckout 9005f761ca592a5d4e6f74400688b135b28800f1で1424テスト・18サブテスト、952.24秒、success。基点PR [#41370846710](https://github.com/kosukeya/t-search/actions/runs/41370846710)はmerge ref c630a15934f2ddaac166ff9558f87b715a0b0bfdで同数、705.59秒、success。今回のheadのCIは[PR #24](https://github.com/kosukeya/t-search/pull/24)へ別記し、基点成功で代用しない。

### 再現コード

リポジトリルートで次のブロックを一時Pythonファイルとして実行する。依存は標準ライブラリと既存のNumPy。ファイル書込み・乱数・実機ショット・旧認定器の呼出しは不要。前回の統計監査もそのまま再実行し、全45条件・21行列条件・反例・照合要約をJSONで標準出力へ返す。

~~~python
import contextlib, io, itertools, json, math, platform
from fractions import Fraction as F
from pathlib import Path
import numpy as np

# Reuse, without editing, the previous inverse and its full verification.
source = Path('docs/t_search_finite_counts.md').read_text().split('~~~python\n')[1].split('\n~~~')[0]
old, captured = {}, io.StringIO()
with contextlib.redirect_stdout(captured):
    exec(compile(source, 'frozen_finite_counts_report', 'exec'), old)
prior = json.loads(captured.getvalue())
lower, combine = old['lower'], old['combine']
TOL = 1e-10

def poisson_binomial(probs):
    mass = [F(1)]
    for p in probs:
        assert F(0) <= p <= F(1)
        out = [F(0)]*(len(mass)+1)
        for k,v in enumerate(mass):
            out[k] += (1-p)*v
            out[k+1] += p*v
        mass = out
    assert sum(mass) == 1
    return mass

def profiles(n,p):
    delta = min(p,1-p)/2
    paired = [p-delta,p+delta]*(n//2)+([p] if n%2 else [])
    total = n*p
    ones = total.numerator//total.denominator
    concentrated = [F(1)]*ones
    if total-ones: concentrated.append(total-ones)
    concentrated += [F(0)]*(n-len(concentrated))
    return [('constant',[p]*n),('paired',paired),('concentrated',concentrated)]

coverage, worst = [], dict(failure_probability=-1.)
for n in (8,25,100):
    thresholds = [F.from_float(lower(k,n)) for k in range(n+1)]
    for p in (F(1,100),F(1,10),F(1,2),F(9,10),F(99,100)):
        for label,probs in profiles(n,p):
            assert len(probs) == n and sum(probs)/n == p
            masses = poisson_binomial(probs)
            if label == 'constant':
                closed = [math.comb(n,k)*p**k*(1-p)**(n-k) for k in range(n+1)]
                assert masses == closed
            failure = sum((v for k,v in enumerate(masses) if thresholds[k] > p), F(0))
            assert failure <= F(1,100)
            row = dict(n=n,mean=str(p),profile=label,failure_probability=float(failure))
            coverage.append(row)
            if row['failure_probability'] > worst['failure_probability']: worst = row

# Full decisions for a flagged phase error, with all five setting streams independent.
n = 25
bad = []
for a,c,b in itertools.product(range(n+1),repeat=3):
    bound = combine([(n,n),(n,n),(a,n),(c,n),(b,n)])['distance_upper']
    if bound is not None and bound < 1: bad.append((a,c,b))
q_profiles = [('constant',[F(1,10)]*n),
              ('alternating',[F(0),F(1,5)]*12+[F(1,10)]),
              ('concentrated',[F(1),F(1),F(1,2)]+[F(0)]*22)]
end_to_end = []
for label,qs in q_profiles:
    assert sum(qs)/n == F(1,10)
    px, pb = poisson_binomial([1-q for q in qs]), poisson_binomial(qs)
    failure = sum((px[a]*px[c]*pb[b] for a,c,b in bad), F(0))
    assert failure <= F(1,20)
    end_to_end.append(dict(profile=label,mean_q='1/10',true_conditional_distance=1,
        false_nontrivial_bound_probability=float(failure)))

# Analytic counterexample if independence is removed, keeping the same marginals.
dependent_failure = sum((F(1,2) for k in (0,100) if F.from_float(lower(k,100)) > F(1,2)),F(0))
assert dependent_failure == F(1,2)

# Qubit matrix checks for the shared-time instrument, independent of the count calculation.
I = np.eye(2,dtype=complex)
X = np.array([[0,1],[1,0]],complex)
Y = np.array([[0,-1j],[1j,0]],complex)
Z = np.diag([1.,-1.]).astype(complex)
probes = [(I+Z)/2,(I-Z)/2,(I+X)/2,(I-X)/2]
inputs = [('plus',probes[2]),('zero',probes[0]),('mixed',(I+.2*X+.3*Y+.4*Z)/2)]
distance = lambda r,s: float(np.abs(np.linalg.eigvalsh(r-s)).sum()/2)
def action(ks,rho): return sum((k@rho@k.conj().T for k in ks),np.zeros((2,2),complex))
def row(*entries):
    # Entry: (public flag, Kraus unitary, squared amplitude).
    return {b:[math.sqrt(float(p))*u for flag,u,p in entries if flag == b and p]
            for b in (0,1)}
good, bad_row = row((0,I,F(1))), row((0,Z,F(1)))
cases = [
    ('all_good',[(1,good)],F(1),F(1),F(0)),
    ('all_Z',[(1,bad_row)],F(0),F(1),F(1)),
    ('alternating',[(1,good),(1,bad_row)],F(1,2),F(1),F(1,2)),
    ('mild_coarse',[(1,good),(1,row((0,I,F(49,50)),(0,Z,F(1,50))))],F(99,100),F(1),F(1,100)),
    ('rare_Z_flag',[(1,row((1,I,F(1)))),(1,row((0,Z,F(1,50)),(1,I,F(49,50))))],F(99,100),F(1,100),F(1)),
    ('branch_weighting',[(1,row((0,I,F(1,4)),(1,I,F(3,4)))),
                         (1,row((0,Z,F(3,4)),(1,I,F(1,4))))],F(5,8),F(1,2),F(3,4)),
    ('late_fault',[(999,good),(1,bad_row)],F(999,1000),F(1),F(1,1000))]
bell = np.array([1,0,0,1],complex)/math.sqrt(2)
bell_state = np.outer(bell,bell.conj())
max_residual, max_excess, equalities, inequalities, zero_time_branches = 0.,0.,0,0,0
def eq(actual,expected):
    global max_residual,equalities
    residual = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
    equalities += 1
    max_residual = max(max_residual,residual)
    assert residual < TOL
def le(actual,bound):
    global max_excess,inequalities
    inequalities += 1
    max_excess = max(max_excess,float(actual-bound))
    assert actual <= bound+TOL

matrix_results = []
for label,groups,fe_ref,mass_ref,z_fraction in cases:
    total = sum(mult for mult,_ in groups)
    for _,inst in groups:
        eq(sum((k.conj().T@k for ks in inst.values() for k in ks),np.zeros((2,2),complex)),I)
    averaged = {b:[math.sqrt(mult/total)*k for mult,inst in groups for k in inst[b]] for b in (0,1)}
    all_k = averaged[0]+averaged[1]
    J = sum((np.kron(k,I)@bell_state@np.kron(k,I).conj().T for k in all_k),np.zeros((4,4),complex))
    fe = float(np.vdot(bell,J@bell).real)
    trace_fe = sum(mult/total*sum(abs(np.trace(k)/2)**2 for ks in inst.values() for k in ks)
                   for mult,inst in groups)
    eq(fe,float(fe_ref)); eq(fe,trace_fe)
    scores = [float(np.trace(r@action(all_k,r)).real) for r in probes]
    eq(scores,[1,1,float(fe_ref),float(fe_ref)])
    eq(sum(scores)/2-1,float(fe_ref))
    for input_label,rho in inputs:
        output = action(averaged[0],rho)
        direct = sum((mult/total*action(inst[0],rho) for mult,inst in groups),np.zeros((2,2),complex))
        eq(output,direct)
        mass = float(np.trace(output).real)
        eq(mass,float(mass_ref))
        normalized = output/mass
        expected_state = (1-float(z_fraction))*rho+float(z_fraction)*Z@rho@Z
        eq(normalized,expected_state)
        d = distance(normalized,rho)
        expected_distance = float(z_fraction)*distance(Z@rho@Z,rho)
        eq(d,expected_distance)
        U = min(1.,math.sqrt(2*(1-float(fe_ref))/float(mass_ref)))
        le(d,U)
        weighted = np.zeros((2,2),complex)
        for mult,inst in groups:
            out_t = action(inst[0],rho)
            p_t = float(np.trace(out_t).real)
            if p_t == 0:
                zero_time_branches += 1
                continue
            weighted += (mult/total*p_t/mass)*(out_t/p_t)
        eq(normalized,weighted)
        matrix_results.append(dict(case=label,input=input_label,blocks=total,Fe=fe,
            p_branch=mass,distance=d,sufficient_upper=U))

# Time conditioning uses posterior mass weights, not equal conditional-state weights.
weight_groups = cases[5][1]
rho = probes[2]
equal_conditionals = sum((action(inst[0],rho)/np.trace(action(inst[0],rho)).real/2
                          for _,inst in weight_groups),np.zeros((2,2),complex))
eq(distance(equal_conditionals,rho),.5)
eq(next(v['distance'] for v in matrix_results if v['case']=='branch_weighting' and v['input']=='plus'),.75)

# Incompatible setting-time weights can invalidate even an average-channel claim.
alias_scores = [float(np.trace(r@u@r@u.conj().T).real) for r,u in zip(probes,(Z,Z,I,I))]
eq(alias_scores,[1,1,1,1])
all_success = combine([(100,100)]*5)
uniform_time_channel = (action([I],rho)+action([Z],rho))/2
alias_true_distance = distance(uniform_time_channel,rho)
eq(alias_true_distance,.5)
assert all_success['distance_upper'] < alias_true_distance

# Same complete tested process, two different next instruments; no current-label leak.
past_A = [I@r@I for r in probes+[rho]]
past_B = [I@r@I for r in probes+[rho]]
for a,b in zip(past_A,past_B): eq(a,b)
future_distances = [distance(u@rho@u.conj().T,rho) for u in (I,Z)]
eq(future_distances,[0,1])
late_bound = combine([(1000,1000)]*2+[(999,1000)]*2+[(1000,1000)])
assert .001 < late_bound['distance_upper'] < 1
new_root_ref = old['decimal_root'](999,1000)
assert F.from_float(lower(999,1000)) <= F(new_root_ref)
new_root_difference = abs(old['raw_lower'](999,1000)-float(new_root_ref))
assert new_root_difference < old['GUARD']

print(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,
    prior_audit=dict(marginal_coverage_cases=prior['marginal_coverage_cases'],
        full_count_decisions=prior['full_count_decisions'],decimal_checks=prior['decimal_checks']),
    heterogeneous_coverage=coverage,worst_coverage=worst,
    full_count_decisions=26**3,nontrivial_decisions=len(bad),end_to_end=end_to_end,
    matrix_cases=matrix_results,equality_checks=equalities,inequality_checks=inequalities,
    max_matrix_residual=max_residual,max_inequality_excess=max_excess,
    zero_time_branches_not_normalized=zero_time_branches,
    alias=dict(observed_scores=alias_scores,pooled_bound=all_success,
               actual_uniform_time_distance=alias_true_distance),
    future=dict(same_past_count_bound=all_success['distance_upper'],next_distances=future_distances),
    dependent_stream_false_lower_probability=float(dependent_failure),
    late_fault_counts=late_bound,new_root_checks=1,new_root_raw_difference=new_root_difference),indent=2))
~~~

## 7. 主張台帳・blockness／becomingへの含意

| ID | 主張 | 根拠と限界 |
| --- | --- | --- |
| TMP-01 | 同分布を固定列の時間変動へ緩め、共通平均を対象にした | §1、(T1)。非適応・独立・共通重みは仮定 |
| TMP-02 | 独立・非同分布Bernoulliの平均に同じKL尾を使える | (T2)–(T3)、Hoeffding Theorem 1。二項分布だとは仮定しない |
| TMP-03 | 前回の数値下限を平均率の下限として再使用できる | 離散尾の解析、45有理数監査。一般性は有限格子によらない |
| TMP-04 | 同じ重みの五率なら平均チャネルのF_eへ接続できる | (T4)、Bell重なりの線形性、前回の校正予算 |
| TMP-05 | 平均インストゥルメントの分枝へ誤差上限を出せる | (T5)、正のr_avgと同時被覆。最小/将来の性能ではない |
| TMP-06 | 平均条件付き状態は分枝確率による重み直しを要する | (T6)、0.25/0.75の対照。零分枝を正規化しない |
| TMP-07 | 45分布・17,576判定/三列・21行列条件を実行した | §4–6、再現コード。実測や全CPTP探索ではない |
| TMP-08 | 平均保証を時刻既知の個別予測へ移せない | 平均距離0.001/最後1、有限上限0.1566の対照 |
| TMP-09 | 設定別の時間重みが違えば合成保証が破れ得る | 全成功なのに真の等重み距離0.5>偽上限0.4342 |
| TMP-10 | 同じ過去の記録だけでは無制約な次の処理を識別できない | 過去I・次I/Zの固定列。将来の独立な制約は追加証拠 |
| TMP-11 | 独立性・校正・期間の指定は同分布と別の信頼条件 | 共通コインの偽下限確率1/2。一般のメモリ保証は未実施 |
| TMP-12 | 予測の適用対象を精密化した一課題を完了した | 全体表現・内部記録・観測者間一致・現実化・存在論は区別 |

全体履歴を表現できることと内部記録が変化することの有限モデルでの両立は既存R4/R5にある。本補足は、記録から許容操作に対する安定した予測を導く際、平均する時間範囲と条件に使える時刻情報が必要になることを示した。全体の平均記述は時刻別の挙動を同一にせず、同じ過去の記録も将来を一意にはしない。

これは観測者間で同じ事実を同定した実験でも、単一事実の現実化の過程でもない。統計的な時間平均、古典的ラベルt、R5の全体履歴、存在論的なadmissible extensions/Actualityを同一視しない。標準の確率・量子形式での適用条件から時間の存在論や新法則を導かない。

**次の判断:** 総括・補足のレビューと統合。適用対象を期間平均・時刻別・将来のどれにするか先に決め、その対象に対する独立性、共通時間重み、校正、必要なら将来の変動制約に、どの独立した実際の証拠を与えられるかを判断する。本報告の固定列・構成カウントはその実証を代替しない。
