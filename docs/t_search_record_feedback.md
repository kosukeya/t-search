# 記録フィードバック下の保証 — 予測可能平均と固定母数の区別

2026-11-04、record-feedback-v1。[実行前プロトコル](t_search_record_feedback_protocol.md)の一課題を完了した。基点は[main 96aea72](https://github.com/kosukeya/t-search/commit/96aea72c205b130e5f6fc83e3abbc415bd5268ab)。[PR #24](https://github.com/kosukeya/t-search/pull/24)は2026-11-03にマージ済みで、R5dと六補足までmainに統合された。前回head 3141b15cf06742867e51300a3817506079aea29cとのtree差分は空。未マージ研究tip・open PRがなかったため、後続の[research/record-feedback-average](https://github.com/kosukeya/t-search/tree/research/record-feedback-average)をmainから作った。

**結論:** 古典的な過去の記録に応じて次の処理を変える場合でも、固定nのマルチンゲール下限から、実現履歴に沿う**予測可能平均インストゥルメント**への条件付き誤差上限を得られる。独立性は要求しないが、現在ブロックの処理を過去から選び、五設定で共用する等の条件は必要。平均はランダムな対象であり、固定未知チャネル、全記録で事後条件付けた出力、次の試行の状態とは別である。

旧KL下限の被覆違反は今回の有限制御クラスでは見つからなかった。この陰性結果を保存し、旧法が一般に安全・危険のどちらとも結論しない。新たな統計定理や物理法則ではなく、既知のマルチンゲール原理と量子上限の適用・限界の監査である。

## 1. 問い・仮定・許容操作

[前回の時間平均](t_search_temporal_average.md)は独立な非適応列だった。今回は、**内部に保存した古典的な記録が後続処理を変える最小モデルで、有限記録から何への保証を維持できるか**を問う。

nと五設定は事前固定。F_(t−1)はブロックt以前の全古典記録である。ブロックtの量子ビットインストゥルメントΦ_t,bはF_(t−1)から選び、そのブロックの五設定に共用する。現在の設定・結果を見て先回りして変更しない。各使用の量子入力/環境はリセットするが、古典的な記憶と制御は次ブロックへ持ち越してよい。ブロック内の同じ処理と、設定/入力の迂回漏れなしは依然仮定である。一般の持越し量子メモリやブロック内の適応は扱わない。

四つの正答ビットと指定入力ρ・公開フラグbのビットをY_t,j∈{0,1}とする。対象の条件付き確率は

$$
p_{t,j}=E[Y_{t,j}\mid F_{t-1}],\quad
\bar p_j(H)=\frac1n\sum_t p_{t,j}(H_{t-1}),\quad
\bar\Phi_b^{\rm pred}(H)=\frac1n\sum_t\Phi_{t,b}(H_{t-1}). \tag{Fbk1}
$$

実現した過去H_(t−1)ごとの予測チャネルを固定して平均する。この経路ごとのCP平均は、未知入力で閉ループ実験全体を再実行したチャネルでも、全過去H_nへ事後選択した装置でもない。そもそもE[K_j/n|F_n]=K_j/nだが、\bar p_j(H)は通常これと異なる。実際の記録から選ばれたランダムな対象への被覆事象を主張している。

固定した実際の準備σ_j・測定効果M̃_jと名目ρ_j・M_j、対象σ/ρ、各ブロック共通の校正上限a_j,m_j,a_*は[校正監査](t_search_calibration_budget.md)から保持する。数値対照は校正予算ゼロ。独立性を過去条件付き期待値の条件へ置き換え、量子的なリセットと古典記憶の保持を区別した。旧R3認定器のsame_cptp_process/reset_between_trials/exact_probabilitiesをTrueにして流用していない。

## 2. 独立性を使わない固定nの下限

一設定についてp_t=E[Y_t|F_(t−1)]、D_t=Y_t−p_tとする。条件付きBernoulliの対数MGFを

$$
h_p(\lambda)=\log(1-p+pe^\lambda)-\lambda p
$$

と置く。h_p(0)=h'_p(0)=0で、二階微分は指数で傾けたBernoulliの分散r(1−r)≤1/4。従ってh_p(λ)≤λ²/8。p=0/1も連続に含む。過去を固定して同じ不等式を使えるので、

$$
E[e^{\lambda D_t}\mid F_{t-1}]\le e^{\lambda^2/8},\qquad
M_t(\lambda)=\exp\!\left(\lambda\sum_{s\le t}D_s-t\lambda^2/8\right)
\tag{Fbk2}
$$

は非負超マルチンゲールになる。独立性による積への因数分解は用いない。固定nでMarkovとλ=4εを使うと

$$
\Pr\!\left(\frac{K}{n}-\bar p(H)>\varepsilon\right)
\le e^{-2n\varepsilon^2}. \tag{Fbk3}
$$

α=0.05を五設定へ配分し、β=α/5=0.01として

$$
\varepsilon_n=\sqrt{\frac{\log(5/\alpha)}{2n}},\qquad
\ell_j=\max(0,K_j/n-\varepsilon_n)
\tag{Fbk4}
$$

を作る。五下限が同時に\bar p_j(H)以下になる確率は1−α以上。クロス設定の独立性も合併則に不要。これは固定計画における無条件の偽保証確率であり、発行後だけの誤認率や事後確率ではない。実験のnを変える任意停止や反復全体への保証は追加していない。

## 3. 経路ごとの量子平均への接続

固定した履歴Hに対して、\barΦ_b^pred(H)はCP、Σ_b\barΦ_b^pred(H)=\barΛ^pred(H)はCPTPである。各過去条件付き実測正答率と理想正答率の差はa_j+m_j以下なので、同時被覆事象上で

$$
s_j=\max(0,\ell_j-a_j-m_j),\quad
L_{\rm pred}=\max\!\left(0,\frac{\sum_js_j}{2}-1\right)
\le F_e(\bar\Lambda^{\rm pred}(H)).
\tag{Fbk5}
$$

Hofmannの名目相補基底の下限を、同じ経路平均へ適用する。Bell重なりの線形性も経路ごとに成り立つ。平均を取る対象の履歴を設定ごとに変えない。

フラグ確率の理想入力の下限はr_pred=max(0,ℓ_b−a_*)。r_pred>0なら、既存の[分枝上限](t_search_branch_bound.md)から

$$
D\!\left(\frac{\bar\Phi_b^{\rm pred}(H)(\rho)}
{\operatorname{Tr}\bar\Phi_b^{\rm pred}(H)(\rho)},\rho\right)
\le\min\!\left(1,\sqrt{\frac{2(1-L_{\rm pred})}{r_{\rm pred}}}\right).
\tag{Fbk6}
$$

r_pred=0ならこの手続きの主張を保留する。実際入力σから名目ρまでの距離は、ℓ_b>0ならmin(1,a_*+sqrt(2(1−L_pred)/ℓ_b))で上から評価する。校正上限自体の推定失敗予算は今回も含めない。

この保証は、各ブロックの処理、次の処理、固定母集団の平均、全履歴で事後条件付けた出力のどれへも無断で移さない。履歴に沿う予測平均を評価するという限定が、独立性を緩める際の対象の型である。

## 4. 旧KLと新下限の最悪方策を正確に比較した結果

n=8,25,100で、p_tを過去から0,1/2,1のいずれかへ選べる有限制御クラスを固定した。S=ΣY、C=2Σpを状態とし、終端を1{ℓ(S,n)>C/(2n)}とする。残りの失敗確率の値関数は、p=0、1/2、1の各次状態の期待値の最大である。終端が(S,C)だけに依存し、許容操作も同じなので、この状態で過去の全記録を圧縮しても最悪値を失わない。

後向きDPでは確率を2^(残り段数)倍した整数で保持。選ばれた方策を別の前向き分布計算で実行し、失敗確率・総確率を完全一致で照合した。n=8では公平ビット列2^8通りをさらに別に実行して一致を確認した。この全ビット列は得た方策の検算であり、全方策を逐次列挙したものではない。方策最適性はBellman再帰が根拠である。

| n | 旧KL下限の最大失敗確率 | 新下限の最大失敗確率 |
| --- | --- | --- |
| 8 | 0.00390625 | 0 |
| 25 | 0.004985272884 | 0.000910520554 |
| 100 | 0.004604879873 | 0.001789930391 |

新下限は全てβ以下。旧KLもこの有限クラスではβを超えなかった。**旧法の反例は見つからなかったという陰性結果**であり、任意のフィードバック確率・長さについてのKL保証を証明したわけではない。前回の独立性を使った証明をそのまま適用できないことと、実際に反例を発見したことを区別する。新下限が最適、全入力で旧法より優れる、という比較でもない。

## 5. 記録が処理を変える量子対照

各ブロックでΦ_t,0=q_t Z(·)Z、Φ_t,1=(1−q_t)id。古典記憶mは初期0で、第五設定のエラーフラグを次の記憶にする。ブロック内では記憶を固定し、X二設定の正答とエラーフラグは条件付き独立に発生させる。三つの規則を固定した。

| 規則 | q(0),q(1) | エラー記録の作用 |
| --- | --- | --- |
| persistent | 0.1,0.9 | エラー後に誤り率が上がる |
| corrective | 0.9,0.1 | エラー後に誤り率が下がる |
| constant | 0.5,0.5 | 記憶への依存がない対照 |

n=4,8,12の全分布を、二つのX正答カウントa,c、エラーカウントb、最終記憶mの有理数DPで求めた。前のエラー数はb−mなので、真の経路平均は[(n−b+m)q(0)+(b−m)q(1)]/n。この式による平均と、後述の明示的な履歴列から求めた平均も照合した。

| 規則 | n | 同時下限の失敗確率 | 保留確率 | 上限1のみの確率 |
| --- | --- | --- | --- | --- |
| persistent | 4 | 0 | 0.9271 | 0.0729 |
| persistent | 8 | 2.3554937284e-05 | 0.75893635 | 0.24106365 |
| persistent | 12 | 9.1641145619e-06 | 0.64093720192 | 0.35906279808 |
| corrective | 4 | 1.9999e-07 | 0.9991 | 0.0009 |
| corrective | 8 | 4.9108728626e-05 | 0.75893635 | 0.24106365 |
| corrective | 12 | 2.0733654736e-05 | 0.097021446562 | 0.90297855344 |
| constant | 4 | 0 | 0.9375 | 0.0625 |
| constant | 8 | 0 | 0.63671875 | 0.36328125 |
| constant | 12 | 0.00073224307562 | 0.38720703125 | 0.61279296875 |

全九条件で同時失敗確率≤α。これらの小標本では誤差1のZ分枝に対する非自明な上限は一度も出ず、偽保証確率も0だった。**保留または自明上限しか出ない**という有用性上の制約も保存する。この零だけで手法の鋭さや一般の失敗率を認定しない。

### 全フラグ履歴の行列照合

三規則×長さ8の全256履歴＝768履歴について、予測されたq列を実際に構成した。＋、0、(I+0.2X+0.3Y+0.4Z)/2の三入力・両分枝の4608条件を、Kraus平均と直接平均で検算した。Bell忠実度、四正答率、分枝確率、正規化状態も別の解析式と比較した。

例えばpersistent規則の00000000では平均q=0.1、01010101では0.4、11111111では0.8。同じ規則でも平均は履歴に依存する。01010101の次の誤り率は0.9であり、平均0.4と同じではない。制御規則そのものを信頼すれば次の率を別途計算できるが、(Fbk6)だけによる将来保証ではない。

21,504比較・4608不等式の最大残差は3.47e-16未満、正の不等式超過は0。有限走査はこのI/Zモデルに限り、一般のCPTP処理への保証は§2–3の解析が根拠である。

## 6. 構成カウントでの保守性

四検査全成功の構成カウントを、固定した七条件へ代入した。各バッチn回で、実測・シミュレーションショット・大量試行の実行報告ではない。これらを上のZ分枝模型で実際に観測したとも扱わない。

| n | フラグ回数 | ε_n | L_pred | r_pred | 条件付き上限 |
| --- | --- | --- | --- | --- | --- |
| 1000 | 1000 | 0.047985259122 | 0.90402948176 | 0.95201474088 | 0.44901627361 |
| 1000 | 10 | 0.047985259122 | 0.90402948176 | 0 | 保留 |
| 100000 | 100000 | 0.0047985259122 | 0.99040294818 | 0.99520147409 | 0.138876388 |
| 100000 | 1000 | 0.0047985259122 | 0.99040294818 | 0.0052014740878 | 1 |
| 20000000 | 20000000 | 0.00033930702122 | 0.99932138596 | 0.99966069298 | 0.036846828333 |
| 20000000 | 200000 | 0.00033930702122 | 0.99932138596 | 0.0096606929788 | 0.37481958786 |
| 4000000000 | 4000000000 | 2.3992629561e-05 | 0.99995201474 | 0.99997600737 | 0.0097965718945 |

この加法余裕による十分上限は保守的で、n=20000000・フラグ頻度1%でも約0.3748。旧独立列用の結果へ独立性を外して同じ精度を無条件に期待しない。最後の40億回という整数例は式の動作確認であり、必要最小試行数・実機計画ではない。全成功・フラグ頻度1ならε_nはn^(-1/2)、この十分上限の主要な減少率はn^(-1/4)になる。定数や方法の最適性は調べていない。

## 7. 一次資料・検証・未実施

Python 3.12.14、NumPy 2.3.5で全条件を実行した。新しく使用した下限161件を80桁Decimalの独立評価と比較し、εは参照値以上、下限は参照値以下だった。最大のε差2.23e-16未満、下限差3.34e-16未満。旧統計監査も凍結コードのまま再実行し、303被覆・17,576判定/5真値・145根の照合を再確認した。数値例の照合を任意入力の形式検証済みソフトウェアとは呼ばない。

掲載コードを抽出して再実行しJSON出力が完全一致した。既存文書整合30ファイルの196 assertion関数を直接呼んで成功（pytest suiteではなく、他モジュール依存3ファイルは対象外）。相対リンク134件、表16個、主張ID12件、ソースhash19項目・参照JSON hash2項目、基点705ファイル中702 blobと旧進捗本文の保持を確認した。変更は既存進捗Markdown 3件への追記と新規Markdown 2件だけで、削除はない。完全な回帰CIは下記の正確なheadと区別する。

公開前のコード差替えで重複挿入を検出したため、単一ブロックへ修正した。境界を行単位で照合してコード全体を抽出し、原本との完全一致と再実行の出力一致を確認した。科学的な計算条件・結果は変えていない。未実行の全ビット検査はJSONでnullとし、失敗と混同しない。

2026-11-04に次の一次資料本文を確認した。

| 資料 | 確認箇所・用途 |
| --- | --- |
| Howard, Ramdas, McAuliffe & Sekhon, [Time-uniform Chernoff bounds via nonnegative supermartingales](https://arxiv.org/pdf/1808.03204)（arXiv v8, 2025-12-17） | §2.1 Definition 1、§3.2 Lemma 3(c)、予測可能な増分の上下幅による分散過程Σ(G+H)^2/4。今回は固定n・幅1だけを自己完結に導出 |
| Hofmann, [Complementary classical fidelities…](https://arxiv.org/pdf/quant-ph/0409083) | 式(14)–(17)、特に(15)。同じ経路平均に対する相補基底の下限 |

古典記録への依存を持つ標準確率/量子モデルへ既知境界を適用した。統計的新規性や独立した新解釈を主張せず、旧KLに関する陰性結果も消していない。

**実行済み:** 導出、六つの最悪方策計算と前向き照合・n=8の全ビット検算、九つのフィードバック全分布、768履歴/4608入力分枝条件、七構成カウント、161高精度比較、旧統計監査、掲載コードの再実行と文書/来歴チェック。最終研究チェックは全て成功し、staged whitespaceも公開前に照合した。

**未実施・保留:** 任意p_tに対する旧KL下限の可否、一般の持越し量子メモリ、ブロック内適応、ブロック固定/リセット/校正/配線の実機認定、任意停止・反復全体への保証、事後状態や将来への保証、物理時計・一事実の現実化の実装。旧R3認定器・固定仕様・コード・テスト・JSONは変更していない。文書のみなのでローカル全体pytestは反復していない。

### 統合とCIの正確な対象

| 対象 | 実際のcheckout | 確認した結果 |
| --- | --- | --- |
| 前回headの[push #41555137084](https://github.com/kosukeya/t-search/actions/runs/41555137084) | 3141b15cf06742867e51300a3817506079aea29c | 1424テスト・18サブテスト、1005.60秒、success |
| 同headの[PR #41555143052](https://github.com/kosukeya/t-search/actions/runs/41555143052) | db1a06329a627e846e30c73220399b3b3cdbd354 | 同数、578.05秒、success |
| PR #24統合の[push #41597784266](https://github.com/kosukeya/t-search/actions/runs/41597784266) | 96aea72c205b130e5f6fc83e3abbc415bd5268ab | 同数、1007.77秒、success |

PR #24の自動コードレビューはhead3141b15に対して指摘なし。科学的な独立査読や本補足の検証結果ではない。本変更の新head/PRのCIは後続PRへ別記し、上の基点成功で代用しない。

### 再現コード

リポジトリルートで次のブロックを一時Pythonファイルとして実行する。標準ライブラリと既存NumPyを使う。乱数・ファイル書込み・実機ショット・旧認定器の呼出しは不要。全監査結果をJSONで標準出力へ返す。

~~~python
import contextlib,io,itertools,json,math,platform
from collections import defaultdict
from decimal import Decimal,localcontext
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import numpy as np

source=Path('docs/t_search_finite_counts.md').read_text().split('~~~python\n')[1].split('\n~~~')[0]
old,captured={},io.StringIO()
with contextlib.redirect_stdout(captured): exec(compile(source,'frozen_finite_counts','exec'),old)
prior=json.loads(captured.getvalue())
TOL=1e-10
up=lambda x:math.nextafter(x,math.inf)
down=lambda x:math.nextafter(x,-math.inf)
def round_down(q):
    f=float(q)
    return down(f) if F.from_float(f)>q else f
@lru_cache(None)
def epsilon(n): return up(math.sqrt(up(up(math.log(100))/(2*n))))
used=set()
@lru_cache(None)
def lower(k,n):
    assert 0<=k<=n and n>0
    used.add((k,n))
    return max(0.,down(round_down(F(k,n))-epsilon(n)))
def combine(counts):
    ell=[lower(k,n) for k,n in counts]
    L=round_down(max(F(0),sum(F.from_float(e) for e in ell[:4])/2-1))
    r=ell[4]
    U=None if r==0 else min(1.,up(math.sqrt(up(up(2*up(1-L))/r))))
    return dict(L=L,r=r,U=U,status='withheld' if U is None else ('trivial' if U==1 else 'nontrivial'))

# Exact worst-case control on p in {0,1/2,1}; probabilities use a common dyadic scale.
def worst_policy(n,kind):
    ell=[F.from_float((old['lower'] if kind=='KL' else lower)(k,n)) for k in range(n+1)]
    terminal=lambda s,c:ell[s]>F(c,2*n)
    nxt={(s,c):int(terminal(s,c)) for s in range(n+1) for c in range(2*n+1)}
    policy={}
    for t in range(n-1,-1,-1):
        now={}
        for s in range(t+1):
            for c in range(2*t+1):
                values=(2*nxt[s,c],nxt[s,c+1]+nxt[s+1,c+1],2*nxt[s+1,c+2])
                action=max(range(3),key=lambda a:values[a])
                now[s,c]=values[action]; policy[t,s,c]=action
        nxt=now
    optimum=nxt[0,0]
    mass={(0,0):1}
    for t in range(n):
        out=defaultdict(int)
        for (s,c),weight in mass.items():
            a=policy[t,s,c]
            if a==0: out[s,c]+=2*weight
            elif a==1: out[s,c+1]+=weight; out[s+1,c+1]+=weight
            else: out[s+1,c+2]+=2*weight
        mass=dict(out)
        assert sum(mass.values())==2**(t+1)
    forward=sum(w for (s,c),w in mass.items() if terminal(s,c))
    assert forward==optimum
    if n==8:
        brute=0
        for bits in itertools.product((0,1),repeat=n):
            s=c=0
            for t,bit in enumerate(bits):
                a=policy[t,s,c]
                s+=bit if a==1 else a//2; c+=a
            brute+=terminal(s,c)
        assert brute==optimum
    result=F(optimum,2**n)
    if kind=='martingale': assert result<=F(1,100)
    return dict(n=n,method=kind,worst_failure=float(result),exact_failure=str(result),
                initial_p=policy[0,0,0]/2,forward_terminal_states=len(mass),
                backward_forward_match=True,all_bits_match=True if n==8 else None)
worst=[worst_policy(n,kind) for n in (8,25,100) for kind in ('KL','martingale')]

# Conditional quantum feedback: two X correctness bits and the error flag per block.
rules=[('persistent',(F(1,10),F(9,10))),('corrective',(F(9,10),F(1,10))),('constant',(F(1,2),F(1,2)))]
joint=[]
for label,(q0,q1) in rules:
    for n in (4,8,12):
        mass={(0,0,0,0):F(1)}
        for t in range(n):
            out=defaultdict(F)
            for (a,c,b,m),weight in mass.items():
                q=(q0,q1)[m]
                for x,y,z in itertools.product((0,1),repeat=3):
                    p=(1-q if x else q)*(1-q if y else q)*(q if z else 1-q)
                    out[a+x,c+y,b+z,z]+=weight*p
            mass=dict(out)
            assert sum(mass.values())==1
        coverage_failure=F(0); false_bound=F(0)
        status=defaultdict(F)
        for (a,c,b,m),weight in mass.items():
            previous_errors=b-m
            mu=((n-previous_errors)*q0+previous_errors*q1)/n
            ell=[F.from_float(lower(k,n)) for k in (a,c,b)]
            if ell[0]>1-mu or ell[1]>1-mu or ell[2]>mu: coverage_failure+=weight
            cert=combine([(n,n),(n,n),(a,n),(c,n),(b,n)])
            status[cert['status']]+=weight
            if cert['U'] is not None and cert['U']<1: false_bound+=weight
        assert coverage_failure<=F(1,20) and false_bound<=F(1,20)
        joint.append(dict(rule=label,n=n,states=len(mass),simultaneous_failure=float(coverage_failure),
                          false_conditional_bound=float(false_bound),
                          decision_probabilities={k:float(v) for k,v in status.items()}))

# All length-eight error histories: matrices use the sequence, DP used b-last.
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1.,-1.]).astype(complex)
probes=[(I+Z)/2,(I-Z)/2,(I+X)/2,(I-X)/2]
inputs=[probes[2],probes[0],(I+.2*X+.3*Y+.4*Z)/2]
bell=np.array([1,0,0,1],complex)/math.sqrt(2)
omega=np.outer(bell,bell.conj())
distance=lambda r,s:float(np.abs(np.linalg.eigvalsh(r-s)).sum()/2)
def action(ks,r): return sum((k@r@k.conj().T for k in ks),np.zeros((2,2),complex))
residual=excess=0.; equalities=inequalities=histories=branch_inputs=0
def eq(a,b):
    global residual,equalities
    err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    residual=max(residual,err);equalities+=1
    assert err<TOL
def le(a,b):
    global excess,inequalities
    excess=max(excess,float(a-b));inequalities+=1
    assert a<=b+TOL
representatives=[]
for label,rule in rules:
    for bits in itertools.product((0,1),repeat=8):
        qs=[];m=0
        for bit in bits: qs.append(rule[m]);m=bit
        mean=sum(qs)/8
        eq(float(mean),float(((8-(sum(bits)-bits[-1]))*rule[0]+(sum(bits)-bits[-1])*rule[1])/8))
        ks={0:[math.sqrt(float(q)/8)*Z for q in qs],1:[math.sqrt(float(1-q)/8)*I for q in qs]}
        all_k=ks[0]+ks[1]
        eq(sum((k.conj().T@k for k in all_k),np.zeros((2,2),complex)),I)
        J=sum((np.kron(k,I)@omega@np.kron(k,I).conj().T for k in all_k),np.zeros((4,4),complex))
        fe=float(np.vdot(bell,J@bell).real)
        eq(fe,1-float(mean))
        scores=[float(np.trace(r@action(all_k,r)).real) for r in probes]
        eq(scores,[1,1,1-float(mean),1-float(mean)])
        for rho in inputs:
            for b in (0,1):
                output=action(ks[b],rho)
                expected_p=float(mean if b==0 else 1-mean)
                direct=sum((float(q if b==0 else 1-q)/8*((Z@rho@Z) if b==0 else rho) for q in qs),np.zeros((2,2),complex))
                eq(output,direct)
                p=float(np.trace(output).real);eq(p,expected_p)
                norm=output/p;target=Z@rho@Z if b==0 else rho
                eq(norm,target)
                eq(distance(norm,rho),distance(target,rho))
                bound=min(1.,math.sqrt(2*float(mean)/expected_p))
                le(distance(norm,rho),bound)
                branch_inputs+=1
        if bits in ((0,)*8,(1,)*8,(0,1)*4):
            representatives.append(dict(rule=label,history=''.join(map(str,bits)),predictable_mean_q=float(mean),
                                        Fe=fe,next_q=float(rule[bits[-1]])))
        histories+=1

examples=[]
for n in (1000,100000,20000000):
    for b in (n,n//100):
        examples.append(dict(n=n,flag_count=b,epsilon=epsilon(n),**combine([(n,n)]*4+[(b,n)])))
n=4000000000
examples.append(dict(n=n,flag_count=n,epsilon=epsilon(n),**combine([(n,n)]*5)))
assert examples[-1]['U']<.01

# Independent 80-digit checks of all lower limits used in the new calculation.
max_epsilon_gap=max_lower_gap=0.
with localcontext() as ctx:
    ctx.prec=80
    for k,n in used:
        ref=(Decimal(100).ln()/(2*Decimal(n))).sqrt()
        assert Decimal.from_float(epsilon(n))>=ref
        ell_ref=max(Decimal(0),Decimal(k)/Decimal(n)-ref)
        assert Decimal.from_float(lower(k,n))<=ell_ref
        max_epsilon_gap=max(max_epsilon_gap,epsilon(n)-float(ref))
        max_lower_gap=max(max_lower_gap,abs(lower(k,n)-float(ell_ref)))
assert max_lower_gap<TOL
print(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,alpha=.05,beta=.01,
    worst_control=worst,feedback_distributions=joint,matrix_histories=histories,branch_input_cases=branch_inputs,
    equality_checks=equalities,inequality_checks=inequalities,max_matrix_residual=residual,max_inequality_excess=excess,
    representative_paths=representatives,constructed_counts=examples,decimal_lower_checks=len(used),
    max_epsilon_gap=max_epsilon_gap,max_lower_gap=max_lower_gap,
    prior_audit={k:prior[k] for k in ('marginal_coverage_cases','full_count_decisions','decimal_checks')}),indent=2))
~~~

## 8. 主張台帳・含意・次の判断

| ID | 主張 | 根拠と限界 |
| --- | --- | --- |
| FBK-01 | 古典記録によるブロック間フィードバックを許した | §1。ブロック内固定・共通五設定・量子リセットは仮定 |
| FBK-02 | 対象は実現履歴に沿う予測可能平均である | (Fbk1)。固定未知チャネル・事後状態・次の処理と別 |
| FBK-03 | 幅1の条件付きMGFから独立性なしの固定n下限を得る | (Fbk2)–(Fbk4)。既知マルチンゲール原理の適用 |
| FBK-04 | 校正補正と量子上限を同じ経路平均へ接続できる | (Fbk5)–(Fbk6)。正の分枝下限と信頼条件が必要 |
| FBK-05 | 有限制御クラスの最悪失敗確率を正確に求めた | 後向き/前向き整数DP、n=8の別実行。任意pの探索ではない |
| FBK-06 | 旧KLの被覆違反は今回見つからなかった | §4。一般の保証または反例として拡張しない陰性結果 |
| FBK-07 | 三規則・三サイズの全分布で同時下限を照合した | §5。有理数全和、小標本では保留/上限1のみ |
| FBK-08 | 768履歴・4608入力分枝条件を行列照合した | §5。I/Zモデルの有限検算で、全体履歴時計の実装ではない |
| FBK-09 | 新下限は構成例で保守性と保留を示した | §6。七整数例は実測・最小試行数ではない |
| FBK-10 | 161下限を高精度で保守側と確認した | §7。一般の形式検証済み認定器は未作成 |
| FBK-11 | 古典記録が後続処理へ作用する模型でも予測対象を分けられる | 経路平均・時刻別・事後・将来の区別。主体間の同一事実は未認定 |
| FBK-12 | 一課題を既知形式の解析・検算として完了した | 単一事実・存在論的becoming・新法則を認定しない |

記録を保存して後続制御へ作用させる有限模型で、履歴に条件付けた予測とその保証を具体化した。全体履歴の表現、内部の記録形成、観測者間の一致、許容操作への予測安定性、単一事実の現実化、存在論的becomingは依然別の主張である。今回の統計的な条件付き期待値を、Actualityが存在論的に生成される過程へ同一視しない。

**次の判断:** この補足のレビュー・統合と、対象を経路平均・固定母集団・事後状態・将来のどれにするかの選択。応用するなら、共通ブロックと古典制御/量子リセット、校正にどの独立した実際の証拠を与えるかを先に固定する。旧KLの一般的可否は未解決として残す。
