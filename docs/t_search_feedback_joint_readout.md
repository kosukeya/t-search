# 記録フィードバック下の分枝状態を同時読出しで保証する

2026-11-07。前回の分枝確率下限に続き、固定入力＋・固定フラグ1で、実現履歴に沿う平均の分枝状態と＋のトレース距離を1/2以下と判定できるか調べた。前回の第五設定を、フラグと出力の目標射影を同じ試行で読む設定に変更した。四つの非選択正答率は今回の判定に使わない。固定長、過去の記録だけでの制御、量子リセット、準備・測定・配線の信頼を仮定した。数値対照の校正誤差は0。[実行前仕様](t_search_feedback_joint_readout_protocol.md) · [前回の分枝確率下限](t_search_feedback_count_bound.md)

## 同時記録からの固定長の保証

試行 $t$ の対象分枝を非正規化CP写像 $\Phi_{t,1}$、入力と目標を純粋状態 $\rho_+=|+\rangle\langle+|$ とする。過去 $F_{t-1}$ から処理が決まるので、フラグと射影失敗の条件付き確率は

$$
p_t=\operatorname{Tr}\Phi_{t,1}(\rho_+),\qquad
e_t=\operatorname{Tr}[(I-\rho_+)\Phi_{t,1}(\rho_+)].
$$

ここで $0\le e_t\le p_t\le 1$。全記録を使い、平均を $\bar p=N^{-1}\sum_t p_t$、$\bar e=N^{-1}\sum_t e_t$ とする。$\bar p>0$ なら、同じ経路の予測可能平均 $\bar\Phi_1=N^{-1}\sum_t\Phi_{t,1}$ を正規化した状態 $\sigma=\bar\Phi_1(\rho_+)/\bar p$ に対し、

$$
q=1-\operatorname{Tr}(\rho_+\sigma)=\bar e/\bar p,\qquad
D(\sigma,\rho_+)=\tfrac12\|\sigma-\rho_+\|_1\le\sqrt q.
$$

分枝内の射影失敗率は、時刻別の失敗率をフラグ確率で重み付けした平均になる。距離不等式は純粋目標のFuchs–van de Graaf上界。原論文 Theorem 1、式(46)の $B$ はroot fidelityで、純粋目標では $B^2=\operatorname{Tr}(\rho_+\sigma)$。同じ後処理と全結果を保持する読出しについて、この距離は予測の全変動距離も上から抑える。さらに後続で選別する場合は別の確率評価が必要になる。[著者論文](https://arxiv.org/pdf/quant-ph/9712042) · [既存の分枝上限](t_search_branch_bound.md)

フラグなし、フラグ付き射影成功、フラグ付き射影失敗に対して倍率 $W_t$ をそれぞれ $1,5/4,1/4$ とする。条件付き平均は $m_t=1+p_t/4-e_t\ge 1/4$。条件付き正規化で $M_t=\prod_{i\le t}(W_i/m_i)$ は初期値1の非負マルチンゲールになる。分枝が未定義の $\bar p=0$、または $q\ge1/4$ の経路では、

$$
\prod_t m_t \le \left(1+\bar p/4-\bar e\right)^N\le1.
$$

従ってそれらの経路で $\prod_t W_t\ge20$ なら $M_N\ge20$。固定 $N$ で $E[M_N]=1$ なので、その共通事象の確率はMarkovの不等式で0.05以下。距離が1/2を超えるには $q>1/4$ が必要なため、未定義を含めた**全経路での誤発行確率は5%以下**。$q=1/4$ での発行も上の確率評価に含まれるが、距離1/2以下という判定には適合する。観測から使うのは積 $\prod_t W_t$ だけで、未知の $m_t$ は証明用。発行条件は成功数 $g$ と失敗数 $b$ の整数比較 $5^g\ge20\cdot4^{g+b}$ であり、失敗がゼロなら14成功から発行する。全試行でフラグ確率0なら積は1で発行しない。

条件付き正規化と非負マルチンゲールは既知の方法である。ここで検証するのは、この読出しを記録フィードバックの分枝状態へ使った場合の発行頻度と識別範囲である。[前回の正規化積の導出](t_search_feedback_count_bound.md)

## 八条件の全経路計算

フラグ確率は初回と直前にフラグがなかったとき $1/4$、直前にフラグがあったとき $1/2$。フラグなしは $Z$、フラグ付きは次のいずれかを各試行で使う。

- 混合操作は確率 $1-\theta$ で $I$、確率 $\theta$ で $Z$。
- コヒーレント操作は $U_\theta=\sqrt{1-\theta}I+i\sqrt\theta Z$。

どちらも、同時記録の三確率は $(1-p_t,p_t(1-\theta),p_t\theta)$。次の設定も同じフラグ履歴で決まるので、**この読出しでの全記録分布は二装置で一致**する。フラグ付き出力は各装置内で時刻によらず、混合では距離 $\theta$、コヒーレントでは $\sqrt\theta$。$\theta=1/2$ では同じ全記録分布の下で距離が $1/2$ と $1/\sqrt2$ に分かれる。$q$ からの平方根上限はこのコヒーレント対照で達成される。追加の出力測定を認めた場合の識別可能性は今回の範囲外。

表は正確な有理数を小数に丸めた。コヒーレント対照で $\theta=1/2$ のときは発行が全て誤りで、混合対照の同じ条件では距離は閾値と等しく誤発行はゼロ。$\theta=1$ は発行ゼロなので条件付きの誤り率は未定義。

| N | θ | 発行確率（両装置） | 無条件誤発行（コヒーレント） | 発行条件付き誤り（コヒーレント） |
| --- | --- | ---: | ---: | ---: |
| 32 | 0 | 0.19293759 | 0 | 0 |
| 32 | 1/4 | 0.00246083 | 0 | 0 |
| 32 | 1/2 | 0.00000625051 | 0.00000625051 | 1 |
| 32 | 1 | 0 | 0 | 未定義 |
| 64 | 0 | 0.94962221 | 0 | 0 |
| 64 | 1/4 | 0.00915685 | 0 | 0 |
| 64 | 1/2 | 0.00000633978 | 0.00000633978 | 1 |
| 64 | 1 | 0 | 0 | 未定義 |

混合対照の無条件誤発行は全八条件でゼロ。境界 $q=1/4$ でも発行はまれだった。$\theta=0$ では64試行で約94.96%発行するが、32試行では約19.29%に留まる。固定倍率の性能をこの八条件で評価した。最適倍率・必要試行数の一般解は保留する。

## 非選択情報との比較、適用範囲

同じ装置で、フラグを捨てた予測可能平均の恒等目標に対する過程忠実度は $F_e=\bar p(1-\theta)$。Bell状態との重なりをKraus表示から計算した。$\bar p\le1/2$ なので、真の $F_e$ と $\bar p$ を既存の十分上限 $\min(1,\sqrt{2(1-F_e)/\bar p})$ に与えても値は1。これは既存の上限式との比較であり、非選択データに基づく全ての手法の限界ではない。同時読出しは指定分枝内の誤りを直接記録する代わりに、入力全体についての保証を持たない。[既存の上限式と適用範囲](t_search_branch_bound.md)

全履歴の表現と、内部の記録が後続処理を選ぶことは、同一の有限模型で両立する。今回の追加はその記録から平均の分枝状態を保証できる操作条件の特定である。測定範囲を固定した識別不能は、別の観測者との一致や、単一事実の現実化についての結果ではない。物理的な記録形成、時刻別・未来への保証、一般の量子メモリ、実機校正、存在論的becomingは保留する。

## 再現・検証

Python 3.12.14、NumPy 2.3.5で下のPythonブロックを実行した。三値の整数DPは各時点で質量を保存し、フラグ数分布と条件付き二項和に分けた計算と八条件全てで厳密一致。24の装置・確率条件で136行列照合を行い、最大絶対差は4.45e−16未満。零確率分枝は正規化していない。固定長の被覆は上の解析で示し、有限計算は対照の性能と識別範囲の検証に使った。掲載コードを単一ブロックから抽出して実行すれば、有理数の発行確率と条件付き誤りを再現できる。

| CI | 実際のcheckout | 結果 |
| --- | --- | --- |
| [基点push](https://github.com/kosukeya/t-search/actions/runs/42139825989) | 76564dd30f41e712af29646bf4fc73be6dc77920 | 1424テスト・18サブテスト成功、748.06秒 |
| [基点PR](https://github.com/kosukeya/t-search/actions/runs/42139833622) | 9ab9bd51aadcbf57901c7dbde49ca35e19b60798 | 1424テスト・18サブテスト成功、947.88秒 |

ローカル全体pytestは環境にpytestがないため未実行。掲載コードと既存文書の照合は実行ログ、新headのCIはPR本文で確認できる。[実行ログ](t_search_research_log.md) · [Draft PR #25](https://github.com/kosukeya/t-search/pull/25)

~~~python
from collections import defaultdict
from fractions import Fraction
from math import comb, sqrt

import numpy as np


def issues(good, bad):
    return 5**good >= 20 * 4**(good + bad)


def joint_probability(n, error_quarters):
    # State is last flag, good count, bad count; mass denominator is 16**t.
    states = {(0, 0, 0): 1}
    for t in range(1, n+1):
        next_states = defaultdict(int)
        for (flag, good, bad), mass in states.items():
            p = 1 + flag  # flag probability in quarters
            for key, weight in [
                ((0, good, bad), 4*(4-p)),
                ((1, good+1, bad), p*(4-error_quarters)),
                ((1, good, bad+1), p*error_quarters),
            ]:
                if weight:
                    next_states[key] += weight * mass
        assert sum(next_states.values()) == 16**t
        states = next_states
    return Fraction(sum(w for (_, g, b), w in states.items() if issues(g,b)), 16**n)


def factorized_probability(n, error_quarters):
    # Enumerate the flag count law alone with rational arithmetic.
    no_flag = [Fraction(1)] + [Fraction(0)]*n
    flagged = [Fraction(0)]*(n+1)
    for t in range(1, n+1):
        no_flag, flagged = (
            [3*a/4+b/2 for a,b in zip(no_flag, flagged)],
            [Fraction(0)] + [no_flag[k]/4+flagged[k]/2 for k in range(n)],
        )
        assert sum(no_flag)+sum(flagged) == 1
    error = Fraction(error_quarters,4)
    # Given the flag path, errors are independent at its flagged positions.
    result = Fraction(0)
    for k, mass in enumerate(a+b for a,b in zip(no_flag, flagged)):
        tail = sum(comb(k,b)*error**b*(1-error)**(k-b)
                   for b in range(k+1) if issues(k-b,b))
        result += mass * tail
    return result


def matrix_controls():
    identity = np.eye(2, dtype=complex)
    z = np.diag([1, -1])
    plus = np.ones((2, 2))/2
    minus = identity-plus
    bell_vector = np.array([1, 0, 0, 1])/sqrt(2)
    bell = np.outer(bell_vector, bell_vector)
    max_error = 0.0
    count = 0

    def check(actual, expected):
        nonlocal max_error, count
        error = float(np.max(np.abs(actual-expected)))
        assert error <= 1e-12
        max_error = max(max_error, error)
        count += 1

    for p in (0, .25, .5):
        for theta in (0, .25, .5, 1):
            for coherent in (False, True):
                if coherent:
                    u = sqrt(1-theta)*identity + 1j*sqrt(theta)*z
                    flagged = [sqrt(p)*u]
                else:
                    flagged = [sqrt(p*(1-theta))*identity, sqrt(p*theta)*z]
                all_kraus = flagged + [sqrt(1-p)*z]
                check(sum(k.conj().T@k for k in all_kraus), identity)
                out = sum(k@plus@k.conj().T for k in flagged)
                check(np.trace(out), p)
                check(np.trace(minus@out), p*theta)
                check(np.trace(plus@out), p*(1-theta))
                choi = sum(np.kron(identity,k)@bell@np.kron(identity,k).conj().T
                           for k in all_kraus)
                check(bell_vector.conj()@choi@bell_vector, p*(1-theta))
                if p:
                    distance = sum(abs(np.linalg.eigvalsh(out/p-plus)))/2
                    check(distance, sqrt(theta) if coherent else theta)
    return count, max_error


assert not issues(0, 0)
assert not issues(13, 0) and issues(14, 0)
print("matrix checks and max absolute error:", matrix_controls())
for n in (32, 64):
    for quarters in (0, 1, 2, 4):
        issue = joint_probability(n, quarters)
        assert issue == factorized_probability(n, quarters)
        if quarters >= 1:
            assert issue <= Fraction(1,20)
        # At theta=1/4, coherent D=1/2 is within the target.
        false_coherent = issue if quarters > 1 else Fraction(0)
        false_mixed = issue if quarters > 2 else Fraction(0)
        print(n, str(Fraction(quarters,4)), str(issue), f"{float(issue):.12g}",
              f"{float(false_coherent):.12g}", f"{float(false_mixed):.12g}",
              str(false_coherent/issue) if issue else "undefined",
              str(false_mixed/issue) if issue else "undefined")
~~~

## 主張台帳

| ID | 主張 | 根拠・範囲 |
| --- | --- | --- |
| FJR-01 | 同時記録から経路平均の比 $q=\bar e/\bar p$ を定義できる | 固定入力、信頼した射影・フラグ、正の分枝質量 |
| FJR-02 | 指定の倍率で全経路の誤発行確率は5%以下 | 条件付き正規化、算術・幾何平均、固定NのMarkov |
| FJR-03 | 良好な64試行対照で発行確率は約94.96% | 八条件の整数DPと独立の有理数照合 |
| FJR-04 | 発行条件付きの誤り率は1にもなり得る | θ=1/2のコヒーレント対照、正の発行確率 |
| FJR-05 | 同じ記録分布で距離が閾値の両側に分かれる | θ=1/2、混合とコヒーレント、指定測定のみ |
| FJR-06 | 既存の非選択上限はこの対照で1 | 真の過程忠実度と平均分枝確率を使った式の比較 |
| FJR-07 | 有限模型で内部記録を使う予測保証を具体化した | 観測者間一致、現実化、存在論的becomingは別の未解決点 |

次は、同時読出しを実機で採用する場合に、準備・射影・フラグ配線の誤差をどこまで独立に制約できるかを判断する。発行後の誤り率も制御したい場合には、それを別の評価条件として指定する必要がある。
