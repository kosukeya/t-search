# 記録フィードバック下の旧KL下限 — 固定長の被覆反例

2026-11-05。[実行前プロトコル](t_search_kl_feedback_protocol.md)に従う一課題の完了報告。基点は[decbbc3089ab8334df48b572f27e28903b7b31ac](https://github.com/kosukeya/t-search/commit/decbbc3089ab8334df48b572f27e28903b7b31ac)、同じ研究ブランチと[Draft PR #25](https://github.com/kosukeya/t-search/pull/25)を継承した。mainは[96aea72c205b130e5f6fc83e3abbc415bd5268ab](https://github.com/kosukeya/t-search/commit/96aea72c205b130e5f6fc83e3abbc415bd5268ab)のまま、R5d・時間平均までの六補足が統合済み。本報告と[前回の記録フィードバック](t_search_record_feedback.md)はPR内の成果である。

**結論:** 独立列で使った片側1%のKL下限を、記録制御の予測可能平均へそのまま移す方法には反例がある。N=1000、活動時p=0.01の固定長制御では、下限が対象平均を超える確率は **0.013552886802066457**。整数による正確な確率和と有理数の対数区間で、1%超えを認証した。前回の有限クラスの陰性結果を保持し、その探索外で適用限界を確定したもので、確率論の新定理・新物理法則とは扱わない。

## 1. 一課題・問い・仮定

問いは「**過去の希少事象を使う固定長の古典記録制御で、旧KL下限は予測可能平均に対し所定の被覆を保つか**」。前回のp_t∈{0,1/2,1}、n≤100では違反が見つからず、任意p_tへの拡張が未解決だった。小さいpと長い期間を事前に固定した明示的な六条件だけで検証する。反例探索のための事後的な条件追加はしていない。

許容操作・対象は前回の古典フィードバック模型を引き継ぐ。全体の試行数Nを先に固定し、過去の記録だけから次の成功確率p_tをpまたは0にする。X_t∈{0,1}、p_t=E[X_t\|F_{t−1}]、S_N=ΣX_t、C_N=Σp_t、対象μ_pred=C_N/Nである。μ_predは実現した過去に沿うランダムな予測可能平均で、固定未知母数・全記録で事後選択した状態・次の試行の確率ではない。

N∈{100,1000,10000}、p∈{1/1000,1/100}、成功数上限K=32、片側予算β=0.01を計算前に固定した。後述の切替後も残りの全試行を確率0で実行し、0結果を全て記録する。実験長の任意停止、試行の破棄、現在の乱数の先取りを許していない。境界認証・独立照合が失敗した条件は保留し、β超えがなければ固定クラスの陰性結果として保存するという成功・中止条件も先に定めた。

## 2. 固定長の切替規則と反例の条件

旧下限ℓ_KL(s,N)は、s>0に対し次の下側の根であり、s=0なら0とする。自然対数を使う。

\[
\operatorname{kl}(x\Vert y)=x\log(x/y)+(1-x)\log((1-x)/(1-y)),\qquad
N\operatorname{kl}(s/N\Vert\ell_{KL})=\log100.
\tag{Klf1}
\]

各s=1,…,32について、s>tpかつN kl(s/N∥tp/N)>log100を満たす最大整数tをg_sとする。sを固定するとこのKL量は0<tp<sで単調減少するので、g_sとg_s+1の符号で境界が確定する。

最初はp_t=p。試行tの終了時に累積成功数sを読み、s>0かつt≤g_sなら次からp_t=0にする。そうでなくてもs=32なら次から0にする。一度0にしたらpへ戻さない。この規則はF_tだけで次の処理を選び、N全体は変えない。τを活動確率pで実行した試行数とすると、C_N=pτ、S_N=S_τ。初到達時は

\[
\ell_{KL}(S_N,N)>\mu_{pred}=p\tau/N.
\tag{Klf2}
\]

上限32に安全に到達した場合、またはNまで継続して初到達しなかった場合は(Klf2)が成立しない。したがって初到達確率がそのまま下限の失敗確率である。規則は制御を止めるが、観測計画の長さは固定Nである。この区別によって、固定長という条件だけでは独立列の下限を移せないことが分かる。

主例N=1000、p=1/100の最初の11境界は、s=1,…,11の順に **[0,7,25,53,87,126,170,217,267,320,375]**。例えば第7試行までに2成功すると切替える。成功数s≤11での互いに排反な初到達だけでも確率は[10070857797,10070857798]/10^12に入り、既に0.01を超える。これは全32境界の集計とは別の部分和証明である。

## 3. 六条件の全経路確率と対照

表の「認証区間」は両端の整数を10^12で割ったもの。整数DPの厳密な分子・分母から外向きに求めた区間であり、浮動小数点の表示丸めに依存しない。β超えも100×分子>分母の整数判定である。六条件全てを保存する。

| N | 活動時p | 旧KLの失敗確率（近似表示） | 認証区間の分子 / 10^12 | β=0.01超え | 非適応の固定p対照 |
| --- | --- | --- | --- | --- | --- |
| 100 | 1/1000 | 0.005582750226707402 | [5582750226,5582750227] | いいえ | 0.00015037636585421186 |
| 100 | 1/100 | 0.006525013042269414 | [6525013042,6525013043] | いいえ | 0.0005345344639930333 |
| 1000 | 1/1000 | 0.009923115558013132 | [9923115558,9923115559] | いいえ | 0.0005880701017629784 |
| 1000 | 1/100 | 0.013552886802066457 | [13552886802,13552886803] | **はい** | 0.0014964815477092432 |
| 10000 | 1/1000 | 0.017472435817944037 | [17472435817,17472435818] | **はい** | 0.000694773668473054 |
| 10000 | 1/100 | 0.015573448890687703 | [15573448890,15573448891] | **はい** | 0.0012007525536900745 |

非適応対照は、pをN回変えず保った独立Bernoulli列の二項上側確率を整数で和したもの。同じKL境界の失敗は六条件ともβ以下で、元の独立列の保証とは整合する。閾値成功数は表の順に3,6,6,21,22,132である。

[前回の加法下限](t_search_record_feedback.md) max(0,S_N/N−sqrt(log100/(2N)))も**同じ制御・同じ終端**に適用した。保守側の丸めを99下限で80桁Decimalと確認し、六条件全てで失敗確率0。ただし正の下限を返す確率も全て0で、この対照では情報がない。これを最適性や実用性の証拠にはしない。任意の固定長予測可能列に対する加法法の正当化は、今回の有限計算ではなく前回の条件付きMGFの解析に依存する。

## 4. 境界と確率の検証方法

**境界:** Fractionによる厳密有理数で、log xの範囲を計算した。x=2^e r、1≤r<2に縮小し、z=(r−1)/(r+1)について

\[
L_m(r)=2\sum_{k=0}^{m-1}\frac{z^{2k+1}}{2k+1},\qquad
0\le\log r-L_m(r)\le\frac{2z^{2m+1}}{(2m+1)(1-z^2)}.
\tag{Klf3}
\]

log2も同じ式で区間化し、負のeでは端点を逆転して加える。40項で全て符号を認証でき、80項への再試行は不要だった。838回の符号検査、最大区間幅2.848e−36未満、符号の最小余裕3.548e−6超。96個の根を80桁Decimalの180回二分法で独立に求め、全て同じ整数境界になった。凍結した[旧実装](t_search_finite_counts.md)の下向きガード付きfloat下限もg_s点で対象を上回り、隣点では上回らないと厳密なfloat→Fraction変換で確認した。理想的な根だけにある丸め反例ではない。

**確率:** p=1/D、D=100または1000とし、時刻tの共通分母をD^tにする。未切替の成功数別整数質量A_t(s)、初到達した成功数別質量B_t(s)、安全に上限32へ到達した質量を保持する。継続中は失敗の重みD−1、成功の重み1で遷移し、既に切替済みの質量はD倍する。これは残りの確率0の記録をそのまま保持する操作である。毎時刻の総質量は厳密にD^tと一致した。分母D^Nの整数分子を加算して全経路の初到達確率を得る。巨大整数を丸めて保存する代わりに、再現出力に分母、分子バイト列のSHA256、外向き区間、成功数別の表示確率を含める。

独立照合は次の通り。

- 80桁Decimalで確率を直接伝播する別の前向き計算との差は最大8.078e−81未満、仕様の1e−50以下。
- N=100の二条件はFractionによる後向き再帰と厳密に一致。N=1000/10000では後向き再帰を実行せず、出力をnullにした。
- 最初の成功だけでの到達質量は1−(1−1/D)^min(N,g_1)と厳密一致。p=1/1000では0.002997001、p=1/100では0。
- 非適応対照の二項確率も整数で集計しβ以下を確認。凍結した旧統計監査の303被覆・17,576判定・145高精度根も変更せず再実行した。

成功数上限の安全停止はN=10000,p=0.01だけにあり、確率約0.9844265511093118。これを失敗に含めていない。無作為モンテカルロは用いていない。

## 5. 量子模型との接続と主張の範囲

各ブロックのインストゥルメントを、履歴依存のp_tに対し

\[
\Phi_{t,0}(\rho)=p_t Z\rho Z,\qquad
\Phi_{t,1}(\rho)=(1-p_t)\rho
\tag{Klf4}
\]

とする。二つのKraus作用素sqrt(p_t)Zとsqrt(1−p_t)Iは完備性を満たす。フラグ0の確率は任意入力でp_t、非選択チャネルの過程忠実度は1−p_t、Z±/X±の四正答率は(1,1,1−p_t,1−p_t)。第五設定のフラグ記録だけで次ブロックのp_tを選ぶ。同じブロック内では五設定の共通処理を固定し、量子入力をリセットし、古典記録を保持するという前回の信頼条件を緩めていない。校正予算はこの対照で0と仮定する。

p_t=0,0.001,0.01と＋、0、(I+0.2X+0.3Y+0.4Z)/2で、完備性・忠実度・四正答率・フラグ確率・正の分枝状態を24行列比較した。最大残差3.34e−16未満、絶対許容差1e−10・相対0。ゼロ確率分枝3件は正規化しない。これにより反例のスコア流を許容する最小CP模型を確認した。

**破れたのは単一スコアのβ=0.01下限を任意の古典フィードバックへ流用できるという主張。** 五設定から作る量子距離の全体予算α=0.05が実際に破れる確率は計算していない。失敗率1.3553%は5%超えではなく、四設定の記録と最終距離式の余裕もある。従って旧五設定手続全体やR3認定器への反証とはしない。全てのKL型マルチンゲール法、固定長手法一般、独立列への元定理を反証したとも言わない。

全体履歴を数式で表すことと、内部記録が後続処理を変えることはこの模型で両立する。しかし観測者間で同一の事実が成立すること、任意の許容操作に対する予測安定性、単一結果の現実化、存在論的becomingは別の問題である。本結果は特に「記録からどの対象への予測保証を述べられるか」に制約を加える。有限模型の一致から時間の存在論を導いていない。

## 6. 一次資料・実行状態・再現手順

- Hoeffding, W. (1963), *Probability inequalities for sums of bounded random variables*, JASA 58, 13–30, [DOI](https://doi.org/10.1080/01621459.1963.10500830)、[著者論文スキャン](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf)。独立性の仮定とp.15 Theorem 1/(2.1)のBernoulli形KL指数を再確認した。今回の適応列にはこの独立性の証明を移せない。
- Howard, Ramdas, McAuliffe and Sekhon, *Time-uniform Chernoff bounds via nonnegative supermartingales*, [著者論文 arXiv:1808.03204](https://arxiv.org/abs/1808.03204)、[PDF](https://arxiv.org/pdf/1808.03204)、§3.2 Lemma 3(c)。予測可能な有界増分の条件付きHoeffding型制御を確認した。今回使う加法法の位置づけを支える一次資料であり、今回の反例を文献上の新発見と扱う根拠ではない。

Python 3.12.14、NumPy 2.3.5で、プロトコルの六条件・境界・確率・対照・量子対応を全て実行し成功した。条件変更・未解決境界はない。掲載コードは凍結した旧有限カウント報告のPythonブロックを読み、その監査も先に実行する。完全な再現出力は下記コードから生成できる。通常数十秒程度で、数万桁の整数を内部に保持するが、巨大整数の十進文字列化はしない。

リポジトリrootで次のコードをPythonとして実行する。報告の`~~~python`から行頭の単独`~~~`までを一度だけ抽出し、例えば `/tmp/kl_feedback_check.py` として保存して `python /tmp/kl_feedback_check.py > /tmp/kl_feedback_result.json` を実行する。抽出元と実行原本を全文比較し、抽出再実行のJSONが一致することを確認する。新しい常設認定器や実験APIは作らず、旧コード・テスト・JSON・過去の台帳を維持する。

~~~python
import contextlib,hashlib,io,json,math,platform
from decimal import Decimal,localcontext
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import numpy as np

source=Path('docs/t_search_finite_counts.md').read_text().split('~~~python\n')[1].split('\n~~~')[0]
old,capture={},io.StringIO()
with contextlib.redirect_stdout(capture): exec(compile(source,'frozen_finite_counts','exec'),old)
prior=json.loads(capture.getvalue())
CAP=32
@lru_cache(None)
def series(x,m):
    z=(x-1)/(x+1); z2=z*z; term=z; total=F(0)
    for k in range(m): total+=term/(2*k+1);term*=z2
    low=2*total
    return low,low+2*term/((2*m+1)*(1-z2))
@lru_cache(None)
def log_bounds(x,m=40):
    assert x>0
    e=0;r=x
    while r>=2:r/=2;e+=1
    while r<1:r*=2;e-=1
    lo,hi=series(r,m);a,b=series(F(2),m)
    return (lo+e*a,hi+e*b) if e>=0 else (lo+e*b,hi+e*a)
sign_checks=0;max_log_width=F(0);min_sign_gap=None
def sign(n,k,c):
    global sign_checks,max_log_width,min_sign_gap
    sign_checks+=1
    if c==0:return 1
    if c>=k:return -1 # One-sided violation requires empirical count > compensator.
    for m in (40,80):
        a,b=log_bounds(F(k)/c,m)
        lo,hi=k*a,k*b
        if k<n:
            a,b=log_bounds(F(n-k)/(n-c),m);lo+=(n-k)*a;hi+=(n-k)*b
        a,b=log_bounds(F(100),m);lo-=b;hi-=a
        max_log_width=max(max_log_width,hi-lo)
        if lo>0 or hi<0:
            gap=lo if lo>0 else -hi
            min_sign_gap=gap if min_sign_gap is None else min(min_sign_gap,gap)
            return 1 if lo>0 else -1
    raise ArithmeticError('Unresolved rational logarithm interval')
@lru_cache(None)
def root80(k,n):
    with localcontext() as ctx:
        ctx.prec=80
        x=Decimal(k)/n; target=Decimal(100).ln()/n
        lo,hi=Decimal(0),x
        for _ in range(180):
            mid=(lo+hi)/2
            value=x*(x/mid).ln()+(1-x)*((1-x)/(1-mid)).ln()
            if value>target:lo=mid
            else:hi=mid
        return (lo+hi)/2
def boundaries(n,d):
    g=[0]
    for k in range(1,CAP+1):
        hint=max(0,min(k*d-1,math.floor(d*n*old['lower'](k,n))))
        while hint>0 and sign(n,k,F(hint,d))<0:hint-=1
        while sign(n,k,F(hint+1,d))>0:hint+=1
        assert sign(n,k,F(hint,d))>0 and sign(n,k,F(hint+1,d))<0
        with localcontext() as ctx:
            ctx.prec=80
            assert hint==int(root80(k,n)*Decimal(n*d))
        # Verify that even the frozen implementation's downward guard still violates.
        assert F.from_float(old['lower'](k,n))>F(hint,d*n)
        assert F.from_float(old['lower'](k,n))<=F(hint+1,d*n)
        g.append(hint)
    return g
def integer_dp(n,d,g):
    active=[1]+[0]*CAP;bad=[0]*(CAP+1);safe=new_bad=0;den=1
    eps=math.nextafter(math.sqrt(math.nextafter(math.nextafter(math.log(100),math.inf)/(2*n),math.inf)),math.inf)
    lows=[]
    for k in range(CAP+1):
        f=float(F(k,n))
        if F.from_float(f)>F(k,n):f=math.nextafter(f,-math.inf)
        lows.append(max(0.,math.nextafter(f-eps,-math.inf)))
    with localcontext() as ctx:
        ctx.prec=80;ref=(Decimal(100).ln()/(2*n)).sqrt()
        assert Decimal.from_float(eps)>=ref
        for k,x in enumerate(lows):assert Decimal.from_float(x)<=max(Decimal(0),Decimal(k)/n-ref)
    for t in range(1,n+1):
        bad=[x*d for x in bad];safe*=d;new_bad*=d;den*=d
        nxt=[0]*(CAP+1)
        for k,a in enumerate(active):
            if not a:continue
            for s,w in ((k,a*(d-1)),(k+1,a)):
                hit=s>0 and t<=g[s]
                if hit or s==CAP:
                    if hit:bad[s]+=w
                    else:safe+=w
                    if F.from_float(lows[s])>F(t,d*n):new_bad+=w
                else:nxt[s]+=w
        active=nxt
        assert sum(active)+sum(bad)+safe==den
    for k,w in enumerate(active):
        if F.from_float(lows[k])>F(1,d):new_bad+=w
    first=den-(d-1)**min(n,g[1])*d**(n-min(n,g[1]))
    assert bad[1]==first
    assert 100*new_bad<=den
    terminal=[active[k]+bad[k]+(safe if k==CAP else 0) for k in range(CAP+1)]
    positive=sum(w for k,w in enumerate(terminal) if lows[k]>0)
    return sum(bad),den,bad,safe,new_bad,positive
def decimal_dp(n,d,g):
    with localcontext() as ctx:
        ctx.prec=80;p=Decimal(1)/d
        a=[Decimal(1)]+[Decimal(0)]*CAP;bad=Decimal(0);safe=Decimal(0)
        for t in range(1,n+1):
            out=[Decimal(0)]*(CAP+1)
            for k,v in enumerate(a):
                if not v:continue
                for s,w in ((k,v*(1-p)),(k+1,v*p)):
                    if s>0 and t<=g[s]:bad+=w
                    elif s==CAP:safe+=w
                    else:out[s]+=w
            a=out
        assert abs(sum(a)+bad+safe-1)<Decimal('1e-70')
        return bad
def backward100(n,d,g):
    @lru_cache(None)
    def value(t,k):
        if t==n:return F(0)
        t1=t+1;s=k+1
        success=F(1) if t1<=g[s] else (F(0) if s==CAP else value(t1,s))
        return (F(d-1)*value(t1,k)+success)/d
    return value(0,0)
def control(n,d):
    lo,hi=math.floor(n/d),n
    while hi-lo>1:
        k=(lo+hi)//2
        if sign(n,k,F(n,d))>0:hi=k
        else:lo=k
    assert sign(n,hi,F(n,d))>0 and sign(n,hi-1,F(n,d))<0
    den=d**n;term=(d-1)**n;cdf=0
    for k in range(hi):
        cdf+=term
        if k+1<hi:
            q,r=divmod(term*(n-k),(k+1)*(d-1));assert r==0;term=q
    fail=den-cdf
    assert 100*fail<=den
    return hi,float(F(fail,den))
results=[];max_decimal_difference=Decimal(0)
for n in (100,1000,10000):
    for d in (1000,100):
        g=boundaries(n,d)
        num,den,hits,safe,newbad,positive=integer_dp(n,d,g)
        with localcontext() as ctx:
            ctx.prec=90;exact_decimal=Decimal(num)/Decimal(den)
            diff=abs(exact_decimal-decimal_dp(n,d,g));max_decimal_difference=max(max_decimal_difference,diff)
            assert diff<Decimal('1e-50')
        if n==100:assert backward100(n,d,g)==F(num,den)
        kstar,control_failure=control(n,d)
        scale=10**12;cert_lo=(num*scale)//den
        subset=sum(hits[:12]);subset_lo=(subset*scale)//den
        results.append(dict(N=n,p=f'1/{d}',cutoffs=g[1:],
            first_hit_probability=float(F(num,den)),probability_interval_1e12=[cert_lo,cert_lo+1],
            exceeds_beta_exact=100*num>den,first_success_probability=float(F(hits[1],den)),
            cap_without_violation_probability=float(F(safe,den)),new_additive_failure=float(F(newbad,den)),
            new_positive_lower_probability=float(F(positive,den)),
            first_11_interval_1e12=[subset_lo,subset_lo+1],first_11_exceeds_beta_exact=100*subset>den,
            independent_control_threshold=kstar,independent_control_failure=control_failure,
            failure_by_count=[float(F(x,den)) for x in hits],
            numerator_sha256=hashlib.sha256(num.to_bytes(max(1,(num.bit_length()+7)//8),'big')).hexdigest(),
            exact_denominator=f'{d}^{n}',decimal_difference=str(diff),backward_match=True if n==100 else None))

# Qubit realization, without claiming a failure of the full five-setting alpha budget.
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.]).astype(complex)
inputs=[(I+X)/2,(I+Z)/2,(I+.2*X+.3*Y+.4*Z)/2]
probes=[(I+Z)/2,(I-Z)/2,(I+X)/2,(I-X)/2]
omega=np.array([1,0,0,1],complex)/math.sqrt(2);bell=np.outer(omega,omega.conj())
max_residual=0.;checks=zero_branches=0
def eq(a,b):
    global max_residual,checks
    e=float(np.max(np.abs(np.asarray(a)-np.asarray(b))));max_residual=max(max_residual,e);checks+=1
    assert e<1e-10
for p in (0.,.001,.01):
    k0,k1=math.sqrt(p)*Z,math.sqrt(1-p)*I
    eq(k0.conj().T@k0+k1.conj().T@k1,I)
    J=sum((np.kron(k,I)@bell@np.kron(k,I).conj().T for k in (k0,k1)),np.zeros((4,4),complex))
    eq(np.vdot(omega,J@omega).real,1-p)
    eq([np.trace(r@(k0@r@k0.conj().T+k1@r@k1.conj().T)).real for r in probes],[1,1,1-p,1-p])
    for rho in inputs:
        out=k0@rho@k0.conj().T;eq(np.trace(out).real,p)
        if p==0:zero_branches+=1
        else:eq(out/np.trace(out).real,Z@rho@Z)
print(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,beta=.01,cap=CAP,
    cases=results,rational_sign_checks=sign_checks,max_log_interval_width=float(max_log_width),
    min_certified_sign_gap=float(min_sign_gap),max_decimal_probability_difference=str(max_decimal_difference),
    inverse_roots_checked=root80.cache_info().currsize,matrix_checks=checks,max_matrix_residual=max_residual,
    zero_branches_not_normalized=zero_branches,
    prior_audit={k:prior[k] for k in ('marginal_coverage_cases','full_count_decisions','decimal_checks')}),indent=2))
~~~

### リポジトリ検証とCI

掲載コードの行頭フェンスを検査して全文抽出し、実行原本と完全一致を確認した。抽出コードの再実行JSONも完全一致。既存文書整合30ファイルの196 assertion関数を直接実行して成功した（pytest suiteではなく、他モジュール依存3ファイルは対象外）。相対リンク140件、表13個の列数、主張ID12件、ソースhash19項目・参照JSON hash2項目を照合した。基点707ファイル中704 blobと旧進捗本文を保持。変更は既存進捗Markdown 3件への追記と新規Markdown 2件で、削除なし。staged whitespaceも確認した。完全な回帰CIは下表の対象と区別する。

| 検証 | 正確な対象 | 状態 |
| --- | --- | --- |
| [基点push CI #41752749791](https://github.com/kosukeya/t-search/actions/runs/41752749791) | `decbbc3089ab8334df48b572f27e28903b7b31ac` | 実checkoutと最終ログを確認。success、1424テスト・18サブテスト、966.15秒 |
| [基点PR CI #41752935597](https://github.com/kosukeya/t-search/actions/runs/41752935597) | merge ref `6e35a066a42a0f63e1ca2740807a95ab743d0da6` | 同確認。success、同数、580.44秒 |
| 本変更の研究計算・文書チェック | 本報告の掲載コードと5 Markdown差分 | ローカル実行済み。詳細は上記 |
| 本変更の完全なpytest / CI | 公開後の研究headとPR merge checkout | ローカル全体pytestは未実行。新headのCIはPR本文に別記し、基点成功で代用しない |

PR #25の開始時点は5 Markdown・1コミット、コメント・submitted reviews・inline threadsは全て0。基点から外部コミット差分は空で、関連未マージ研究tipはこのブランチだけ。mainと研究ブランチのREADME/roadmap、最新プロトコル・報告・台帳、PR本文・差分・レビュー、CIを実際に確認した。上位とリポジトリ内にAGENTS.mdはなかった。

**未実施・保留:** 五設定の全体α違反確率、より鋭い有効な適応下限、一般の量子メモリ・ブロック内適応、校正/共通ブロック/リセット/配線の実機認定、物理ショット、実験長の任意停止・反復全体の保証、事後状態・将来への保証、物理時計・単一事実・存在論的becoming。今回の既知条件での否定的/非情報的結果も保存した。

## 7. 主張台帳と次の判断

| ID | 主張 | 根拠・適用限界 |
| --- | --- | --- |
| KLF-01 | 六条件の希少事象制御を計算前に固定した | 実行前仕様。前回の探索外だけを限定して追加 |
| KLF-02 | 全N試行を保持する予測可能制御である | §1–2。切替は過去のみ。実験長の任意停止ではない |
| KLF-03 | 初到達が旧KL下限の失敗と同値である | (Klf1)–(Klf2)、単調性、上限/未到達の区別 |
| KLF-04 | 全境界を有理数の対数区間で認証した | §4、96独立Decimal根。floatガードでも同じ符号 |
| KLF-05 | N=1000,p=0.01で失敗確率は1%を超える | 正確な整数DP、外向き区間、s≤11の部分和でも超える |
| KLF-06 | 六条件中三つがβ超え、三つは超えなかった | §3の全結果。任意の最悪方策の最適化ではない |
| KLF-07 | 独立な固定p対照は全てβ以内だった | 厳密二項和。元の独立列の定理は保持 |
| KLF-08 | 同じ終端の加法下限は失敗0だが全て下限0 | 正確な経路集計、99保守側照合。実用性は未確立 |
| KLF-09 | スコア流は許容するCPインストゥルメントで実現できる | (Klf4)、24行列比較。実機認定ではない |
| KLF-10 | 五設定の全体5%量子誤差違反は示していない | §5。単一βの反例と全体αを区別 |
| KLF-11 | 前回の有限クラスの陰性結果は変更しない | p_t∈{0,1/2,1}、n≤100の範囲のまま保持 |
| KLF-12 | 予測保証の適用限界を一段階具体化した | 全体表現・内部記録・主体間一致・予測安定性・現実化・存在論を分離 |

**次の判断:** 同じPRの総括と補足をレビューし、一般の古典記録フィードバックには旧KL下限の無条件な流用を採用しないという適用条件を確定する。有効だが保守的な加法下限を維持するか、特定の予測対象と許容制御を固定してより鋭い保証を別途監査するかを選ぶ。実機へ進む場合の独立した信頼条件の証拠は依然必要である。
