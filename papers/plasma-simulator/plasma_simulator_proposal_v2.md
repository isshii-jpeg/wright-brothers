# 自律進化型マルチスケール・マルチフィジックス プラズマシミュレーター設計提案書

**Version:** 2.0 — 技術課題分析とソフトウェア・ブレイクスルー戦略  
**Date:** 2026-04-02  
**前提文書:** 設計提案書 v1.0 (2026-04-01)  
**Scope:** v1.0で提示した3本柱（AMMC・PINO・自律進化ループ）の実現を阻む技術的ボトルネックの特定と、2024–2026年の最新研究成果に基づくブレイクスルー戦略の提示

---

## 目次

1. [はじめに：v1.0からの問い](#1-はじめにv10からの問い)
2. [技術課題の体系的分類](#2-技術課題の体系的分類)
3. [課題I：AMMC境界の保存則整合性](#3-課題iammc境界の保存則整合性)
4. [課題II：PINOの長時間安定性と汎化](#4-課題iipino の長時間安定性と汎化)
5. [課題III：自律進化ループの信頼性](#5-課題iii自律進化ループの信頼性)
6. [課題IV：ソフトウェア基盤の微分可能性](#6-課題ivソフトウェア基盤の微分可能性)
   - 6.4 [Reality Check：JAX移行における実装上の落とし穴](#64-reality-checkjax移行における実装上の落とし穴)
7. [課題V：エクサスケール計算への接続](#7-課題vエクサスケール計算への接続)
8. [統合アーキテクチャの再設計提案](#8-統合アーキテクチャの再設計提案)
9. [改訂ロードマップ](#9-改訂ロードマップ)
10. [結論](#10-結論)
11. [参考文献](#11-参考文献)

---

## 1. はじめに：v1.0からの問い

v1.0では、核融合プラズマの $10^8$ に及ぶ時空間スケール隔差を突破するために、適応的ミクロ-マクロ結合（AMMC）、Physics-Informed Neural Operator（PINO）、自律進化ループの3本柱を提案した。本稿では、**v1.0の構想を実装に移す際に直面する技術的ボトルネック**を体系的に整理し、2024–2026年に発表された最新の研究成果を踏まえて、**どのようなソフトウェア上のブレイクスルーがあれば各フェーズを前進させられるか**を具体的に論じる。

本稿の立場は明確である：v1.0の数理的枠組みは健全だが、**実装上の5つの壁**がプロトタイプから実用コードへの道を阻んでいる。これらの壁は、物理学の問題というよりもソフトウェア工学と計算科学の問題であり、近年の急速な進歩によって突破の現実的な道筋が見えてきた。

---

## 2. 技術課題の体系的分類

v1.0の実装を阻む技術課題を、影響度と解決の見通しに基づいて5つに分類する：

| ID | 課題 | 影響するフェーズ | 現在の成熟度 | ブレイクスルーの距離 |
|----|------|-----------------|-------------|-------------------|
| I | AMMC境界の保存則整合性 | Phase 1–2 | 理論定式化済み、実装未検証 | **近い** |
| II | PINOの長時間安定性と汎化 | Phase 2–3 | 1D検証段階 | **中程度** |
| III | 自律進化ループの信頼性 | Phase 3 | 概念実証なし | **遠い** |
| IV | ソフトウェア基盤の微分可能性 | 全フェーズ | v1.0で未考慮 | **近い** |
| V | エクサスケール計算への接続 | Phase 4 | 既存コードに知見蓄積 | **近い** |

以下、各課題について現状の壁、最新研究が示す突破口、そして具体的なソフトウェア設計への含意を論じる。

---

## 3. 課題I：AMMC境界の保存則整合性

### 3.1 壁の本質

v1.0 §3.1.2で、MHD↔運動論セルの境界におけるChapman-Enskog展開による速度分布関数の構成と、ラグランジュ未定乗数法による保存則強制を提案した。しかし、実装上の困難は以下の点にある：

1. **Chapman-Enskog展開の打ち切り誤差**: 強い非平衡（$\mathcal{D} \sim \epsilon_{\text{kin}}$）の境界付近では、展開の低次打ち切りが非物理的な速度分布を生成する。特にビーム成分やテール粒子がこの展開で表現できない。

2. **ラグランジュ乗数法の計算コスト**: 各境界面・各タイムステップで制約付き最適化を解く必要があり、AMMCの動的セル再分類が高頻度で発生する場合、境界処理がボトルネック化する。

3. **遷移領域のアーティファクト**: MHDからPICへの急激な切り替えは、数値的な反射波やスプリアス振動を生む。v1.0のバッファゾーン提案は定性的であり、定量的な設計指針が不在。

### 3.2 最新研究が示す突破口

**muphyIIコード (Allmann-Rahn et al., 2024)** は、まさにこの問題に対する実装レベルの回答を提示した最初のコードの一つである。muphyIIは、運動論から流体まで複数の物理モデル階層を統一フレームワーク内で扱い、局所条件に基づいてサブドメインごとに適切なモデルを動的に選択する。v1.0のAMMCコンセプトと極めて近い設計思想であり、**大規模HPCシステム上での動作実績**がある点が重要である。

さらに、**Haahr, Gudiksen & Nordlund (2025)** によるDISPATCHフレームワーク内のPIC-MHD結合は、太陽フレアシミュレーションにおいてPICとMHDの自己無撞着な結合を実現し、プラズマ振動・二流体不安定性・電流シート再結合の検証テストを通過している。

**非線形ベンチマーク (Reviews of Modern Plasma Physics, 2025)** では、HYMAGYC（MHD-ジャイロ運動論）、MEGA（MHD-ドリフト運動論）、ORB5（全電磁ジャイロ運動論PIC）、XTOR-K（二流体MHD+完全運動論PIC）の4コードが、NLED-AUGケースで相互検証された。この結果は、**異なる結合戦略の定量的な精度比較**を初めて提供するものであり、AMMC設計時の判断基準として極めて有用である。

### 3.3 ソフトウェア設計への含意

v1.0のAMMC設計を以下のように改訂すべきである：

**改訂1: 段階的遷移層（Graduated Transition Layer; GTL）の導入**

Chapman-Enskog展開の急激な打ち切りではなく、muphyIIの知見を参考に、MHDセルとPICセルの間に**3層の遷移ゾーン**を設ける：

$$\text{MHD} \xrightarrow{\text{Layer 1}} \text{Extended MHD} \xrightarrow{\text{Layer 2}} \text{Gyrokinetic (δf)} \xrightarrow{\text{Layer 3}} \text{Full PIC}$$

各層の幅は局所的なイオンラーモア半径 $\rho_i$ の倍数で定義し、遷移関数にはerror function型のスムーズな重み付けを適用する：

$$w(\mathbf{x}) = \frac{1}{2}\left[1 + \text{erf}\left(\frac{d(\mathbf{x}) - d_0}{\sigma}\right)\right]$$

ここで $d(\mathbf{x})$ は最近接境界面からの距離、$d_0$ は遷移中心、$\sigma \sim \rho_i$ は遷移幅である。

**改訂2: 保存則強制の2段階化**

ラグランジュ乗数法による厳密な保存則強制は、毎ステップではなく $N_{\text{correct}}$ ステップごとに実行する。ステップ間では、**局所的なフラックス整合**（境界面を横切る粒子フラックスとMHDフラックスの一致）のみを簡易的に課す。これにより計算コストを $O(1/N_{\text{correct}})$ に削減しつつ、長時間での保存則ドリフトを抑制する。

---

## 4. 課題II：PINOの長時間安定性と汎化

### 4.1 壁の本質

v1.0 §3.2で提案したPINOベースのVlasov方程式サロゲートには、以下の根本的な課題がある：

1. **自己回帰的ロールアウトの誤差蓄積**: PINOを $f(t_n) \mapsto f(t_{n+1})$ の時間ステッパーとして使用する場合、予測誤差が各ステップで蓄積し、長時間シミュレーションで発散する。これはニューラル演算子サロゲートに共通する本質的な問題である。

2. **保存量のドリフト**: v1.0の損失関数に $\mathcal{L}_{\text{conservation}}$ と $\mathcal{L}_{\text{entropy}}$ を含めたが、これらはソフト制約であり、ハード制約ではない。$10^6$ ステップの積分後に保存量が物理的に許容できない範囲にドリフトするリスクがある。

3. **分布外汎化**: PINOのオフライン学習に使用するPICデータは必然的に限られたパラメータ空間をカバーする。シミュレーション中に未知の物理レジーム（例：予期しない不安定性の非線形飽和）に遭遇した場合、PINOの予測信頼性が保証できない。

### 4.2 最新研究が示す突破口

**Gopakumar et al. (Nuclear Fusion, 2024)** は、Fourier Neural Operator（FNO）をプラズマ進化のサロゲートとして適用し、従来のMHDソルバーに対して**6桁の高速化**を達成した。MAST Tokamakの実験データへの適用も含み、ゼロショット超解像にも対応する。しかし同時に、長時間ロールアウトの精度劣化が報告されている。

この問題に対する直接的な回答が、**ニューラル演算子のプラズマエッジシミュレーションサロゲート (arXiv:2502.17386, 2025)** の研究である。JOREK MHDコードとSTORMコードに対するFNOサロゲートにおいて、**低忠実度から高忠実度データへの転移学習**が、小規模データセットでの誤差を1桁低減することを示した。重要なのは、**長時間自己回帰ロールアウトの精度劣化と誤差蓄積が依然として主要な課題である**と明確に指摘している点である。

一方、**構造保存型ニューラルネットワーク**の分野で画期的な進展がある：

- **Dong et al. (Physics of Plasmas, 2025)** は、シンプレクティック行列ネットワーク（SympMat）とHénonネットワーク（HenonNet）を開発し、電磁場中の荷電粒子ダイナミクスに適用した。SympMatはサブジャイロ周期スケールまでBorisプッシャーを上回る精度を達成している。これは**PICシミュレーションの軌道積分器として直接適用可能**である。

- **Liang et al. (Scientific Reports, 2025)** のSPINIは、教師なしでハミルトニアンを学習し、吉田4次シンプレクティック積分器に埋め込むことで、パラメトリック摂動下でも構造保存を実現する。

- **Symplectic Gyroceptron (Scientific Reports, 2023; follow-up 2024–2025)** は、準周期的シンプレクティック写像を近似する構造保存ニューラルネットワークを構成し、磁気閉じ込め装置中の荷電粒子ダイナミクスに直接関連する長時間忠実度を保証する。

さらに、**FNOベースのVlasovモーメントクロージャ (Huang et al., 2025)** は、低次流体モーメントから熱フラックス勾配への写像をFNOで学習し、線形・非線形Landau減衰の両方で検証した。これはv1.0 §3.2.3で「PINO適用: Yes」としたクロージャモデルの**具体的な実装の先行事例**である。

### 4.3 ソフトウェア設計への含意

**改訂3: ハイブリッド時間積分器 — PINO + シンプレクティック補正**

v1.0のPINO時間ステッパー $\mathcal{G}_\theta : f(t_n) \mapsto f(t_{n+1})$ を、以下のハイブリッド構造に置き換える：

$$f(t_{n+1}) = \underbrace{\mathcal{S}}_{\text{シンプレクティック補正}} \circ \underbrace{\mathcal{G}_\theta(f(t_n))}_{\text{PINO予測}}$$

ここで $\mathcal{S}$ は、SympMatまたはHenonNet型のシンプレクティックネットワークであり、PINOの出力を**正準構造を保存する最近接写像**に射影する。これにより：

- PINOが提供する高速な近似を活用しつつ、
- シンプレクティック補正がハミルトン構造（位相空間体積保存、エネルギー保存の長時間安定性）を強制する。

この二段構成の計算コストは、シンプレクティック補正がPINO推論の $O(10\%)$ 以下であるため、v1.0の計算コスト削減目標を大きく損なわない。

**改訂4: 不確実性定量化に基づく動的PICフォールバック**

PINOの予測に対してMonte Carlo Dropout（またはDeep Ensemble）による不確実性推定を付与し、以下の判定を自動化する：

$$\text{if } \sigma_{\text{PINO}}(\mathbf{x}, t) > \sigma_{\text{threshold}}: \quad \text{switch to PIC at } (\mathbf{x}, t)$$

これはv1.0のリスク緩和策「PICフォールバック機構を常に維持」を、**定量的・自動的な判定基準**に昇格させるものである。$\sigma_{\text{threshold}}$ はAMMCの非平衡度指標 $\mathcal{D}$ と同列に、AIによる動的校正の対象とする。

**改訂5: 転移学習パイプラインの設計**

FNOサロゲートの転移学習が小規模データセットで1桁の誤差低減をもたらすという知見 (arXiv:2502.17386) を活用し、PINOの学習を以下の3段階に構造化する：

1. **ステージ1（汎用ベース）**: 1D/2D Vlasov-Poisson問題の大規模データセットでベースモデルを事前学習
2. **ステージ2（物理特化）**: 対象とする物理現象（例：GEM再結合、ELMサイクル）の高忠実度PICデータで転移学習
3. **ステージ3（オンライン適応）**: v1.0で提案したオンライン学習機構により、実行時に微調整

---

## 5. 課題III：自律進化ループの信頼性

### 5.1 壁の本質

v1.0 §5のAuto-researchフィードバックループは、本提案の最も野心的な要素であると同時に、最も実現が不確実な要素である。具体的な壁：

1. **LLMの物理的推論の信頼性**: Model Critic（§5.3）がLLMに物理モデルの分析を依頼する際、LLMの出力が物理的に正しい保証がない。ハルシネーションが物理モデルの修正提案に混入した場合、シミュレーション全体の信頼性が損なわれる。

2. **Code Synthesizerの堅牢性**: 自然言語の修正提案を正しいコードパッチに変換する信頼性が未検証。特に、数値的に微妙なアルゴリズム（例：暗黙解法の前処理変更）の自動生成は、現在のLLMの能力では品質保証が困難。

3. **検証のスケーラビリティ**: §5.4の安全弁（保存則ハードリミット、リグレッションテスト）は必要条件だが十分条件ではない。テストを通過する誤った物理モデル（overfitting to benchmarks）のリスクがある。

### 5.2 最新研究が示す突破口

この領域では3つの重要な進展がある：

**MCP-SIM (Park, Moon & Ryu, npj Artificial Intelligence, 2026)** は、マルチエージェントLLMフレームワークにより、自然言語プロンプトから検証済み物理シミュレーションへの変換を実現した。反復的な「計画-実行-反省-修正」サイクルと、エージェント間の永続的メモリを用いて、12タスクのベンチマークで**100%の成功率**を達成した。ただし、対象は比較的単純な物理シミュレーションであり、核融合プラズマのような複雑系への適用可能性は未検証である。

**Scientific Generative Agent (SGA; Ma et al., ICML 2024)** は、LLMによる離散的な科学仮説提案と、微分可能シミュレーションによる連続パラメータ最適化を**二層最適化**として定式化した。構成則の発見や分子設計において、人間の予想と異なるが物理的に整合的な解を発見している。この枠組みは、v1.0のAuto-researchループに対して、**LLMの提案を微分可能シミュレーションで定量的に検証する**というアーキテクチャの改訂を示唆する。

**AI Scientist-v2 (Lu et al., Sakana AI, 2025)** は、仮説生成から論文執筆までの完全自律的な科学的発見システムであり、ICLR 2025ワークショップで人間の査読を通過した初のAI生成論文を生み出した。しかし、独立した評価 (arXiv:2502.14297) では**42%の実験失敗率**（コーディングエラー起因）と、文献レビューにおける新規性評価の不十分さが指摘されている。

### 5.3 ソフトウェア設計への含意

**改訂6: 二層最適化アーキテクチャへの移行**

v1.0の直列パイプライン（Diagnostics → Model Critic → Code Synthesizer → Test）を、SGAに着想を得た**二層最適化構造**に再設計する：

```
Upper Level: LLM (Model Critic)
  │
  │  propose: 離散的モデル構造変更
  │  (例: "衝突演算子にLenard-Bernstein近似を導入")
  │
  ▼
Lower Level: Differentiable Simulation (微分可能シミュレータ)
  │
  │  optimize: 連続パラメータの勾配最適化
  │  (例: 衝突周波数 ν の最適値を自動微分で決定)
  │
  ▼
Validation Gate: 保存則 + リグレッションテスト + PIC参照解との比較
```

この構造の利点：
- LLMは**離散的な構造提案**のみを担い、数値的に微妙な連続パラメータの決定は自動微分に委ねる
- 「LLMが物理的に間違った提案をしても、微分可能シミュレータが連続最適化で救済できる」安全網が形成される
- 検証ゲートで棄却された場合のフィードバックが、LLMの次の提案を改善する

**改訂7: 信頼度階層型自動適用ポリシー**

v1.0では「パラメータ微調整のみ自動適用、構造変更は人間承認」という二値的なポリシーだったが、以下の4段階に細分化する：

| 信頼度レベル | 変更種別 | 適用方式 | 例 |
|-------------|---------|---------|-----|
| **L4 (自動)** | 連続パラメータの微調整 | 即座に全域適用 | PINO学習率、閾値 $\epsilon_{\text{MHD}}$ |
| **L3 (限定自動)** | 既知パターンの選択 | 限定領域で検証後、自動展開 | 衝突演算子の切り替え（BGK↔Fokker-Planck）|
| **L2 (提案)** | 新項の追加・既存項の修正 | 人間承認 + 限定領域検証 + 段階的展開 | 新しい不安定性駆動項の導入 |
| **L1 (報告)** | 方程式系の構造変更 | 人間による詳細レビュー必須 | 基礎方程式の変更、新変数の導入 |

---

## 6. 課題IV：ソフトウェア基盤の微分可能性

### 6.1 壁の本質 — v1.0の盲点

v1.0では、C++/CUDAコアの高性能計算、Julia接着層、Python AIオーケストレーションという3層構成を提案した。しかし、**シミュレーション全体を通した自動微分（AD）の可能性**が考慮されていない。これは2024–2026年の研究動向に照らして、重大な設計上の見落としである。

微分可能性が欠如していることの具体的な影響：

1. **PINOの学習**: 現在の設計では、PINOの学習データはPICシミュレーションの出力を事後的に収集する。シミュレーション自体が微分可能であれば、**end-to-endの勾配最適化**が可能になり、PINOの学習効率が劇的に向上する。

2. **パラメータ最適化**: 自律進化ループ（§5）でのパラメータ調整が、勾配なしの探索（Grid Search、Bayesian Optimization）に限定される。微分可能であれば勾配降下法が使用でき、パラメータ空間の探索効率が指数的に向上する。

3. **逆問題**: 実験データからプラズマパラメータを推定する逆問題（例：Thomson散乱データからの速度分布関数再構成）に、シミュレーターを直接利用できない。

### 6.2 最新研究が示す突破口 — 微分可能プラズマシミュレーションの台頭

2024–2026年は、プラズマ物理における微分可能プログラミングの「離陸の年」と位置づけられる：

**Differentiable Programming for Plasma Physics (arXiv:2603.11231, 2026)** は、このパラダイムを体系的に実証した画期的な論文である。4つの応用を示している：

1. **微分可能運動論シミュレーションの最適化**による、未知の超加法的波束相互作用レジームの発見
2. 流体シミュレーションにおける**時空間非局所的な運動論的効果を捉える隠れ変数の学習**
3. Thomson散乱解析の**140倍高速化**と、~1000パラメータの速度分布関数抽出
4. 時空間レーザーパルスの**逆設計**

**TORAX (Citrin, Goodfellow et al., Google DeepMind, 2024)** は、JAXによるオープンソースの微分可能トカマクコア輸送シミュレーターである。イオン/電子熱輸送、粒子輸送、電流拡散の結合方程式を解き、JAXのJITコンパイルによる高速実行と、自動微分による勾配ベース最適化・ヤコビアンベースPDE解法を実現した。RATPORコードとの検証も完了している。

**JAX-in-Cell (Ma et al., 2025)** は、JAXによる完全電磁・多粒子種・相対論的1D3V PICフレームワークである。**本質的に微分可能**であり、レーザーパルス形状のend-to-end勾配最適化、実験データからのパラメータ発見、PINNループ内へのPIC埋め込みが可能。CPU、GPU、TPUで動作する。

### 6.3 ソフトウェア設計への含意 — JAXベース再設計の提案

**改訂8: コア計算エンジンのJAX移植**

v1.0の言語構成を根本的に再考する必要がある。具体的には、以下の段階的移行を提案する：

```
v1.0 設計:
  Python (orchestration) → Julia (glue) → C++/CUDA (core)

v2.0 設計:
  Python/JAX (orchestration + core + AD) → C++/CUDA (性能臨界カーネルのみ)
```

**根拠:**

JAXは以下の利点を同時に提供する：

| 特性 | C++/CUDA | Julia | JAX |
|------|----------|-------|-----|
| 自動微分 | 手動実装が必要 | ForwardDiff/Zygote（制限あり）| ネイティブ対応 |
| GPU対応 | ネイティブ | CUDA.jl（成熟度中）| XLA経由で透過的 |
| TPU対応 | 非対応 | 非対応 | ネイティブ対応 |
| JITコンパイル | コンパイル時最適化 | JIT（初回遅延）| XLA JIT |
| PINOとの統合 | FFI必要 | FFI必要 | 同一フレームワーク |
| エコシステム | 巨大 | 中規模 | PyTorch/TF互換 |

**ただし、JAXへの全面移行には注意点がある：**

- AVX-512やNUMA-awareメモリ配置のような**低レベル最適化はJAXでは困難**。性能臨界な粒子プッシャーカーネルは、JAX custom call機構を通じてC++/CUDAカーネルを呼び出す設計とする。
- JAX-in-Cell (2025) が1D3Vで成功しているが、**3Dフルスケールへのスケーラビリティは未実証**。Phase 1のMVPで2D検証を行い、Phase 2で3D拡張の可否を判断する。

**改訂9: 微分可能性を活用した新しいPINO学習パイプライン**

シミュレーション全体が微分可能になることで、PINOの学習を以下のように革新できる：

```
従来（v1.0）:
  PIC実行 → データ保存 → PINO学習（事後的）

改訂（v2.0）:
  微分可能PIC ←→ PINO（end-to-end勾配伝播）
     ↓
  ∂L/∂θ を直接計算：PINOパラメータθの更新に、
  PICの物理的勾配情報を利用
```

これは、JAX-in-CellがPINNループ内へのPIC埋め込みを可能にしたことの直接的な拡張であり、**PINO学習の収束速度とデータ効率を飛躍的に向上**させる。

### 6.4 Reality Check：JAX移行における実装上の落とし穴

§6.3でJAXベースへの移行を提案したが、ここでは率直にその実装上の「絶望的な相性問題」と、それに対する具体的な設計戦略を論じる。v2.0の構想が「論文上の美しさ」で終わらないためには、この節が最も重要である。

#### 6.4.1 落とし穴1：JAXの静的Shape要求 vs AMMCの動的メッシュ

**問題の本質**

JAXの強みであるXLAコンパイラは、計算グラフのコンパイル時に**すべての配列の形状（Shape）が確定**していることを要求する。`jax.jit` でコンパイルされた関数に異なるShapeの入力を渡すと、再コンパイル（re-tracing）が発生し、コンパイルキャッシュが無効化される。

一方、AMMCの本質は**物理状態に応じた動的なメッシュ再構成**である：

- 非平衡度 $\mathcal{D}$ が閾値を超えたセルは細分化（refinement）される → 配列サイズが増加
- $\mathcal{D}$ が閾値を下回ったセルは粗視化（coarsening）される → 配列サイズが減少
- PICセルでは粒子数が動的に変動する → 粒子配列のサイズが不定

これはJAXのXLAコンパイルモデルと**根本的に衝突**する。素朴にJAXで実装すると、メッシュが変化するたびにre-tracingが発生し、コンパイル時間がシミュレーション時間を上回る「コンパイル地獄」に陥る。

**v2.0の解決戦略：3層ハイブリッドアーキテクチャ**

この問題に対して、「全部JAXにする」アプローチも「JAXを諦める」アプローチも採らない。以下の**3層分離アーキテクチャ**を提案する：

```
┌──────────────────────────────────────────────────────────────┐
│  Layer A: Mesh Orchestrator（非JAX — Pure Python / C++）      │
│  ─────────────────────────────────────────────────────────── │
│  • AMMCのメッシュ管理（セルの生成・消滅・再分類）              │
│  • AMRの再分割判定（Wavelet error estimator）                 │
│  • Hilbert曲線負荷分散の再計算                                │
│  • ドメイン間のゴースト交換のオーケストレーション              │
│  → JAXの外側で実行。静的Shape制約なし。                       │
│  → 頻度：Nrebalanceステップに1回（典型的に100–1000ステップ）   │
└─────────────────────────┬────────────────────────────────────┘
                          │ 固定サイズの「パッチ」を発行
                          ▼
┌──────────────────────────────────────────────────────────────┐
│  Layer B: Patch Solver（JAX — JITコンパイル済み）              │
│  ─────────────────────────────────────────────────────────── │
│  • 固定サイズのパッチ上で物理ソルバーを実行                    │
│  • 完全に微分可能（jax.grad, jax.vjp が利用可能）             │
│  • パッチサイズはバケットシステムで管理（後述）                │
│  → XLAが最大効率で動作する「安全圏」                          │
└─────────────────────────┬────────────────────────────────────┘
                          │ 勾配情報を返却
                          ▼
┌──────────────────────────────────────────────────────────────┐
│  Layer C: Performance Kernels（C++/CUDA — JAX custom call）   │
│  ─────────────────────────────────────────────────────────── │
│  • Boris粒子プッシャー（AVX-512 / CUDAカーネル）              │
│  • FFTベース場ソルバー（cuFFT）                               │
│  • NUMA-awareメモリ管理                                       │
│  → JAX custom_call + custom_vjp で微分可能性を維持            │
└──────────────────────────────────────────────────────────────┘
```

**核心的な設計判断**：AMMCのメッシュ管理（動的部分）と物理計算（静的部分）を**明確に分離**する。物理計算はすべて「固定サイズのパッチ」上で実行し、JAXのXLAコンパイルが最大効率で動作する領域に閉じ込める。

**バケットシステムによるパッチサイズ管理**

完全に任意のサイズのパッチを許容すると、パッチごとにre-tracingが必要になる。これを回避するために、**離散的なサイズバケット**を事前定義する：

| バケットID | セルサイズ (2D) | セルサイズ (3D) | 用途 |
|-----------|----------------|----------------|------|
| B0 | $32 \times 32$ | $16 \times 16 \times 16$ | MHDセル（粗い格子） |
| B1 | $64 \times 64$ | $32 \times 32 \times 32$ | ジャイロ運動論セル |
| B2 | $128 \times 128$ | $64 \times 64 \times 64$ | PICセル（細かい格子） |
| B3 | $256 \times 256$ | $128 \times 128 \times 128$ | 高解像度PICセル |

各バケットに対して `jax.jit` コンパイル済みのソルバーカーネルを**事前に用意**する。AMMCの再分割時に、各セルは最も近いバケットサイズに**切り上げ**られ、余剰セルはパディング + マスクで処理する：

```python
# 概念的なコード
@functools.partial(jax.jit, static_argnums=(0,))
def solve_patch(bucket_id: int, field_data, particle_data, mask):
    """bucket_idは静的引数 → バケットごとにコンパイル（計4回のみ）"""
    # mask: [Nx, Ny] boolean array — パディング領域をFalseに
    # field_data: 固定Shape [bucket_Nx, bucket_Ny, n_fields]
    # particle_data: 固定Shape [max_particles_per_bucket, 6]
    
    field_update = mhd_or_pic_solver(field_data, particle_data)
    return jnp.where(mask[..., None], field_update, field_data)  # マスク適用
```

**パディングによるメモリオーバーヘッドの定量的評価：**

最悪ケースでは、各パッチがバケットの下限ぎりぎりのサイズで、次のバケットに切り上げられる。たとえばB0（$32^2$）に対して実際のセルが $33 \times 33$ の場合、B1（$64^2$）にパディングされ、メモリ効率は $33^2 / 64^2 \approx 27\%$ まで低下する。

しかし現実には：
- AMMCの再分割はoctree/quadtreeベースであり、セルサイズは2のべき乗の近傍に集中する
- バケット間隔を2倍（$32, 64, 128, ...$）ではなく $\sqrt{2}$ 倍（$32, 48, 64, 96, 128, ...$）にすれば、最悪ケースのオーバーヘッドは $\sim 50\%$ に改善される（バケット数は7–8に増加）
- パディング領域の計算は実行されるが、結果はマスクで捨てられるため、**正しさには影響しない**

**推奨構成**: $\sqrt{2}$ 間隔のバケット（7–8バケット）で開始し、プロファイリング結果に基づいてバケット数を調整する。JITコンパイルのウォームアップ（全バケットの初回コンパイル）はPhase 0で実施し、実行時のre-tracingをゼロにする。

**粒子数の動的変動への対処**

PICセル内の粒子数は物理的に変動する（電離・再結合、セル間移動）。これに対しては**Arenaアロケーション方式**を採用する：

```python
# 各PICパッチに固定サイズの粒子アリーナを割り当て
particle_arena = jnp.zeros([MAX_PARTICLES_PER_PATCH, 6])  # 固定Shape
particle_count = jnp.int32(actual_count)                   # 実際の粒子数
validity_mask = jnp.arange(MAX_PARTICLES_PER_PATCH) < particle_count

# Boris pusher はアリーナ全体に適用（無効粒子も計算するが結果を捨てる）
new_positions, new_velocities = boris_push(particle_arena, E, B)
particle_arena = jnp.where(validity_mask[:, None], 
                           jnp.concatenate([new_positions, new_velocities], axis=-1),
                           particle_arena)
```

`MAX_PARTICLES_PER_PATCH` は各バケットに対して統計的に設定する。典型的なPICシミュレーションでは、セルあたり粒子数（PPC: Particles Per Cell）は $\sim 100$ で設計するため：

$$\text{MAX\_PARTICLES\_PER\_PATCH} = \alpha \cdot \text{PPC} \cdot N_{\text{cells\_per\_patch}}$$

ここで $\alpha \sim 1.5\text{–}2.0$ はオーバーフロー安全率。$\alpha$ を超えた場合は、Layer Aのオーケストレーターがパッチを分割する（次の再分割タイミングを待たず即座に実行）。

**JAXの動的Shape対応の将来的な展望**

JAX 0.4.x 系以降、`jax.experimental.sparse` や `jax.pure_callback` による部分的な動的Shape対応が進行中である。特に：

- **`jax.pure_callback`**: 任意のPython関数をJIT内から呼び出し可能（ただし微分不可）。Layer Aのメッシュ判定ロジックをJIT内で呼ぶ「脱出口」として利用可能。
- **Shape polymorphism (`jax.export`)**: 限定的だが、コンパイル時にShape未確定のままexportする機能。将来的にバケットシステムを不要にする可能性がある。

ただし、これらは2026年4月時点で実験的機能であり、**本プロジェクトのPhase 1–2ではバケットシステムを前提として設計し、JAXの動的Shape対応が成熟した時点で移行を検討する**のが安全なアプローチである。

#### 6.4.2 落とし穴2：Backprop Through Time によるVRAM枯渇

**問題の本質**

プラズマシミュレーションの典型的なタイムステップ数を考える：

| 物理現象 | 時間スケール | イオンスケールΔt | ステップ数 |
|---------|------------|----------------|----------|
| Landau減衰（検証用） | $\sim 100 \omega_{pe}^{-1}$ | $10^{-10}$ s | $\sim 10^3$ |
| 磁気再結合 | $\sim 10^{-4}$ s | $10^{-8}$ s | $\sim 10^4$ |
| ELMサイクル | $\sim 10^{-2}$ s | $10^{-8}$ s | $\sim 10^6$ |
| 電流拡散 | $\sim 1$ s | $10^{-8}$ s | $\sim 10^8$ |

逆伝播（Backpropagation Through Time; BPTT）では、各タイムステップの中間状態（活性化値）をメモリに保持する必要がある。1ステップの状態が $S$ バイトの場合、$N$ ステップのBPTTには $O(N \cdot S)$ のメモリが必要になる。

具体的な見積もり（Phase 2のGEM再結合問題、2D、$128^2$ グリッド、PPC=100）：

$$S_{\text{fields}} \approx 128^2 \times 8 \text{ fields} \times 8 \text{ bytes} \approx 1 \text{ MB}$$
$$S_{\text{particles}} \approx 128^2 \times 100 \times 6 \times 8 \text{ bytes} \approx 600 \text{ MB}$$
$$S_{\text{total}} \approx 600 \text{ MB/step}$$

$10^4$ ステップのBPTTでは：

$$\text{VRAM}_{\text{naive}} \approx 600 \text{ MB} \times 10^4 = 6 \text{ TB}$$

これは現存するどのGPUのVRAMも超えている（H100: 80 GB、A100: 80 GB）。**ナイーブなBPTTは完全に不可能**である。

**v2.0の解決戦略：4段構えのメモリ管理**

**戦略1: `jax.checkpoint`（勾配チェックポインティング / 再物質化）**

最も基本的かつ効果的な対策。タイムステップを $K$ ステップごとのセグメントに分割し、セグメント境界のみ中間状態を保持する。逆伝播時に、各セグメント内の中間状態を再計算（rematerialization）する：

```python
from jax import checkpoint

def simulate_segment(state, n_steps_per_segment):
    """1セグメント（K ステップ）のシミュレーション"""
    def body_fn(i, state):
        return one_timestep(state)
    return jax.lax.fori_loop(0, n_steps_per_segment, body_fn, state)

@jax.jit
def simulate_with_checkpointing(initial_state, n_segments, K):
    """全体シミュレーション（チェックポイント付き）"""
    def segment_fn(state, _):
        # checkpoint: 順伝播時は中間状態を破棄、逆伝播時に再計算
        next_state = checkpoint(simulate_segment)(state, K)
        return next_state, None
    final_state, _ = jax.lax.scan(segment_fn, initial_state, None, length=n_segments)
    return final_state
```

メモリ/計算のトレードオフ：

| チェックポイント間隔 $K$ | メモリ使用量 | 計算オーバーヘッド |
|--------------------------|-------------|-------------------|
| 1（チェックポイントなし） | $O(N \cdot S)$ | 0% |
| $\sqrt{N}$ | $O(\sqrt{N} \cdot S)$ | $\sim 100\%$（2倍の計算） |
| $N$（1セグメント） | $O(S)$ | $\sim (N-1) \times 100\%$ |
| **最適: $K = \sqrt{N}$** | **$O(\sqrt{N} \cdot S)$** | **$\sim 100\%$** |

GEM再結合の例（$N = 10^4, S = 600$ MB）：

$$K = \sqrt{10^4} = 100, \quad \text{セグメント数} = 100$$
$$\text{VRAM} \approx 100 \times 600 \text{ MB} = 60 \text{ GB} \quad (\text{H100に収まる})$$
$$\text{計算オーバーヘッド} \approx 2\times \quad (\text{許容範囲})$$

**戦略2: 多段チェックポインティング（Binomial Checkpointing）**

$\sqrt{N}$ チェックポイントでもVRAMが不足する大規模問題では、**再帰的なチェックポインティング**を適用する。Griewankのbinomial checkpointing (treeverse) アルゴリズムにより、$m$ 個のチェックポイントスロットで $O(m \cdot \log N)$ の計算オーバーヘッドでメモリを $O(m \cdot S)$ に抑制できる：

$$\text{VRAM}_{\text{binomial}} = m \cdot S, \quad \text{計算} = O\left(\frac{N \log N}{m}\right) \cdot (\text{1ステップのコスト})$$

ELMサイクル（$N = 10^6$）でも、$m = 50$ スロット（$\sim 30$ GB）で実行可能になる。

JAXでは `jax.checkpoint` のネストにより近似的に実現可能であり、より厳密な実装として **Diffrax** ライブラリの `diffrax.RecursiveCheckpointAdjoint` が利用できる。

**戦略3: Truncated BPTT + 短ホライズン勾配**

そもそも、**シミュレーション全体を通した勾配が本当に必要か？**を問い直す。

v2.0で勾配を利用する主要な場面を再整理する：

| 用途 | 必要な勾配のホライズン | 全ステップBPTT必要？ |
|------|----------------------|---------------------|
| PINOのオンライン学習 | $\sim 10\text{–}100$ ステップ | **No** |
| 自律進化ループのパラメータ最適化 | $\sim 100\text{–}1000$ ステップ | **No** |
| 初期条件の逆問題 | 全ステップ | **Yes（チェックポイント必須）** |
| レーザーパルス設計（将来） | 全ステップ | **Yes（チェックポイント必須）** |

大半のユースケースでは、**Truncated BPTT（短いウィンドウでの勾配計算）** で十分である：

```python
# Truncated BPTT: Twindowステップごとに勾配を計算・適用
T_window = 50  # 50ステップの勾配ウィンドウ

for segment_start in range(0, total_steps, T_window):
    # 順伝播（T_windowステップ分、勾配追跡あり）
    loss, grads = jax.value_and_grad(simulate_segment)(state, T_window)
    
    # パラメータ更新（PINOの重み、物理パラメータ等）
    params = optimizer.update(grads, params)
    
    # stateはdetach（勾配グラフを切断）して次のセグメントへ
    state = jax.lax.stop_gradient(state)
```

VRAM使用量は常に $O(T_{\text{window}} \cdot S)$ に固定され、$T_{\text{window}} = 50$ なら $\sim 30$ GB で収まる。

**戦略4: 随伴法（Adjoint Method）による定常問題の効率化**

Phase 4のトカマク安定性解析のように、**定常状態の感度解析**が目標の場合は、離散随伴法（discrete adjoint method）が最適である。BPTTとは異なり、随伴方程式を**逆向きに1パスで**解くため、メモリ使用量は順伝播と同程度で済む：

$$\text{VRAM}_{\text{adjoint}} = O(S) \quad (\text{1ステップ分の状態 + 随伴変数})$$

JAXでは `jax.custom_vjp` を用いて随伴法を明示的に実装できる。また、Diffrax の `diffrax.BacksolveAdjoint` が微分方程式の随伴解法を提供する。

**推奨される段階的適用**

| フェーズ | メモリ戦略 | 理由 |
|---------|-----------|------|
| Phase 0–1 | Truncated BPTT ($T_w = 50$) | 検証問題は小規模。VRAM問題が発生しにくい |
| Phase 2 | `jax.checkpoint` ($K = \sqrt{N}$) | PINO学習の長ホライズン化に伴いチェックポイントが必要に |
| Phase 3 | Binomial checkpointing | 自律進化ループの大規模パラメータ探索 |
| Phase 4 | 随伴法 | 定常状態の安定性解析。$10^6$+ ステップ |

#### 6.4.3 両落とし穴の交差：動的メッシュ上のチェックポインティング

2つの落とし穴は**独立ではない**。AMMCによるメッシュ再構成が発生すると、チェックポイント地点の状態と現在の状態で**配列構造が異なる**可能性がある。これは逆伝播時に深刻な問題を引き起こす。

**解決策: メッシュ再構成タイミングとチェックポイント境界の同期**

```
Time →
├──── Segment 1 ────┤──── Segment 2 ────┤──── Segment 3 ────┤
│ メッシュ固定        │ メッシュ固定        │ メッシュ固定        │
│ JAX JIT内で計算    │ JAX JIT内で計算    │ JAX JIT内で計算    │
├───────────────────┤───────────────────┤───────────────────┤
↑                   ↑                   ↑
Checkpoint          Checkpoint          Checkpoint
+ Mesh rebalance    + Mesh rebalance    + Mesh rebalance
(Layer A で実行)    (Layer A で実行)    (Layer A で実行)
```

各セグメント内ではメッシュ構造は**完全に固定**される（Layer B: JAX JITの安全圏）。セグメント境界でのみ、Layer Aのメッシュオーケストレーターがメッシュ再構成を行い、同時にチェックポイントを保存する。

逆伝播時には：
1. チェックポイントから状態を復元
2. そのチェックポイント時点のメッシュ構造を復元（メッシュ構造自体もチェックポイントに含める）
3. セグメント内の中間状態を再計算（メッシュは固定なのでJIT内で実行可能）
4. セグメント内の勾配を計算
5. セグメント間の勾配はメッシュ変換のヤコビアンを通じて接続

セグメント間の勾配接続において、メッシュ変換（補間・制限操作）のヤコビアンが必要になる。これは `jax.custom_vjp` で明示的に実装する：

```python
@jax.custom_vjp
def mesh_transform(old_state, old_mesh, new_mesh):
    """メッシュ再構成に伴う状態の補間"""
    return interpolate(old_state, old_mesh, new_mesh)

def mesh_transform_fwd(old_state, old_mesh, new_mesh):
    result = mesh_transform(old_state, old_mesh, new_mesh)
    # 逆伝播に必要な情報を保存
    return result, (old_mesh, new_mesh)

def mesh_transform_bwd(res, g):
    old_mesh, new_mesh = res
    # 補間のヤコビアン転置を適用（逆方向の補間 = restriction操作）
    old_grad = restrict(g, new_mesh, old_mesh)
    return old_grad, None, None

mesh_transform.defvjp(mesh_transform_fwd, mesh_transform_bwd)
```

この設計により、**メッシュが動的に変化するシミュレーション全体を通した勾配計算**が、JAXの静的Shape制約と矛盾なく実現可能になる。

#### 6.4.4 リスク評価の更新

§6.4の議論を踏まえ、v2.0のリスクマトリクスを更新する：

| リスク | 影響度 | 発生確率 | 緩和策 |
|--------|--------|---------|--------|
| バケットシステムのメモリオーバーヘッドが許容範囲を超える | 中 | 低 | $\sqrt{2}$ 間隔バケットで最悪50%。プロファイリングに基づき調整 |
| JITコンパイル時間がウォームアップで問題になる | 低 | 中 | 7–8バケット × 3物理モデル = 20–24回のコンパイル。Phase 0で事前実行 |
| メッシュ再構成とチェックポイントの同期が性能ボトルネックに | 中 | 中 | セグメント長 $K$ を再構成頻度に合わせて調整。最悪ケースでも計算量2倍 |
| JAXの将来的な動的Shape対応がバケットシステムを陳腐化 | 低 | 高 | Layer A/B分離により、JAX側の変更がLayer Aに影響しない設計 |
| Truncated BPTTの勾配バイアスがPINO学習を阻害 | 中 | 中 | Phase 2以降でチェックポイント付き全ステップBPTTに段階的移行 |

---

## 7. 課題V：エクサスケール計算への接続

### 7.1 壁の本質

v1.0のPhase 4では、マルチGPU（4–8 GPU）スケーリングを目標としている。しかし、核融合プラズマの実用的な安定性解析（ITERスケール）には、数千GPU以上のエクサスケール計算が必要になる。v1.0のアーキテクチャがエクサスケールに拡張可能かは不明である。

### 7.2 最新研究が示す突破口

**WarpXのエクサスケール達成 (2024–2025)** は、PICコードのエクサスケール動作が現実であることを実証した。Frontier（AMD MI250X GPU）での全スケール実行に成功し、2016年の開始以来**500倍の性能改善**を達成している。20段連続レーザー駆動プラズマ加速の模擬を可能にした。

**XGCのFrontier実績 (2024–2025)** では、乱流によるダイバータ熱負荷幅の予測が実験的に検証された。**Kokkosによるポータビリティ**と、Ginkgoバッチ反復解法の組み合わせにより、AMD GPUへの移植を実現している。

**Fortranプラズマコードのエクサスケール移植 (2024)** は、OpenMPオフローディングとKokkos抽象層の両方を用いたAMD GPUへの移植戦略を実証し、レガシーコードの移行障壁に対する実践的解答を提供している。

### 7.3 ソフトウェア設計への含意

**改訂10: パフォーマンスポータビリティ層の導入**

v1.0のCUDA直書き戦略を改め、以下の2層構成とする：

```
Application Layer (JAX / Python)
    │
    ▼
Portability Layer (Kokkos / XLA backend)
    │
    ├── NVIDIA GPU: CUDA backend
    ├── AMD GPU:    HIP backend
    ├── Intel GPU:  SYCL backend
    └── CPU:        OpenMP backend
```

JAXのXLAバックエンドは本質的にマルチベンダーGPU対応だが、性能臨界カーネル（粒子プッシャー）についてはKokkosラッパーを用意し、WarpXやXGCの実績ある最適化パターンを活用する。

**改訂11: エクサスケール学習データパイプラインの確立**

v1.0 §3.2.4で「高精度PICシミュレーション（既存コード: VPIC, OSIRIS等）の結果からベースモデルを事前学習」と記述したが、これをエクサスケール計算リソースと明示的に接続する：

- **WarpXをPINO学習データの主要生成源として位置づける**。WarpXはすでにFrontier上で実動しており、大規模な高忠実度PICデータを生成できる。
- Apache Arrowベースのzero-copy IPCに加え、**ADIOS2**（Adaptable IO System）を導入し、WarpXの出力をストリーミングで受け取るインターフェースを構築する。ADIOS2はWarpXの標準出力フォーマットであり、追加開発なしで接続可能。

---

## 8. 統合アーキテクチャの再設計提案

v1.0とv2.0の改訂を統合した新しいシステムアーキテクチャを以下に示す：

```
┌──────────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                            │
│                   Python (asyncio + Ray)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │  Workflow     │  │  Bilevel      │  │  Diagnostics +       │  │
│  │  Control      │  │  Optimizer    │  │  Anomaly Detection   │  │
│  │              │  │  (LLM+AD)    │  │                       │  │
│  └──────┬───────┘  └──────┬───────┘  └───────────┬───────────┘  │
│         │                 │                       │              │
├─────────┼─────────────────┼───────────────────────┼──────────────┤
│         │     Differentiable Compute Engine       │              │
│         ▼                 ▼                       ▼              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    JAX Core Layer                         │   │
│  │  - AMMC domain decomposition + GTL transitions           │   │
│  │  - Differentiable PIC (JAX-in-Cell extended)             │   │
│  │  - MHD solver (JAX-CFD patterns)                         │   │
│  │  - IMEX time integrator                                  │   │
│  │  - End-to-end autodiff through full simulation           │   │
│  └────────────┬───────────────────┬─────────────────────────┘   │
│               │                   │                              │
│  ┌────────────▼────────┐  ┌──────▼──────────────────────┐      │
│  │  C++/CUDA Kernels   │  │  PINO + Symplectic Layer    │      │
│  │  (via JAX custom    │  │  - FNO/DeepONet surrogate   │      │
│  │   call + Kokkos)    │  │  - SympMat/HenonNet correct │      │
│  │  - Boris pusher     │  │  - Uncertainty quantifier   │      │
│  │  - FFT field solver │  │  - FNO closure model        │      │
│  │  - SIMD MHD Riemann │  │                              │      │
│  └─────────────────────┘  └──────────────────────────────┘      │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                    Data / Memory Layer                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Apache Arrow (zero-copy IPC) + ADIOS2 (WarpX連携)      │   │
│  │  + HDF5 (checkpoint) + Redis (metrics) + W&B (AI logs)  │   │
│  └──────────────────────────────────────────────────────────┘   │
├──────────────────────────────────────────────────────────────────┤
│              Portability Layer (XLA + Kokkos)                     │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │ NVIDIA GPU │ │  AMD GPU   │ │ Intel GPU  │ │    CPU     │   │
│  │   (CUDA)   │ │   (HIP)    │ │   (SYCL)   │ │  (OpenMP)  │   │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### v1.0→v2.0 主要変更点のサマリー

| 要素 | v1.0 | v2.0 | 変更の根拠 |
|------|------|------|-----------|
| コア計算 | C++/CUDA | JAX + C++/CUDAカーネル | 微分可能性の確保（§6） |
| 接着層 | Julia | JAX（Juliaは廃止） | 言語間IPC削減、AD一貫性 |
| PINO時間ステッパー | DeepONet単体 | DeepONet/FNO + シンプレクティック補正 | 長時間安定性（§4） |
| AMMC境界 | Chapman-Enskog + ラグランジュ乗数 | GTL段階的遷移 + 2段階保存則強制 | 境界アーティファクト低減（§3） |
| 自律進化ループ | 直列パイプライン | 二層最適化（LLM+AD） | LLM信頼性の補償（§5） |
| GPU戦略 | CUDA直書き | XLA + Kokkos（マルチベンダー） | エクサスケール接続（§7） |
| 学習データ | 自前PIC生成 | WarpX/ADIOS2パイプライン | エクサスケール既存資産の活用（§7） |
| 不確実性 | なし | MC Dropout / Deep Ensemble | 動的PICフォールバック判定（§4） |
| クロージャモデル | PINO（概念） | FNOベースクロージャ（先行実装あり） | Huang et al. (2025) の知見（§4） |

---

## 9. 改訂ロードマップ

v1.0のフェーズ構造を維持しつつ、v2.0の改訂を反映した新ロードマップ：

### Phase 0: 基盤整備（3ヶ月） — 改訂

| タスク | v1.0からの変更 |
|--------|--------------|
| JAX開発環境構築 | **新規**: JAX + jaxlib (CUDA/ROCm) + Flax/Equinox のセットアップ |
| JAX-in-Cell評価 | **新規**: JAX-in-Cellの2D拡張可能性の技術評価。Landau減衰、二流体不安定性で微分可能PICの動作確認 |
| WarpX-ADIOS2連携 | **新規**: WarpXの出力をADIOS2経由でストリーミング受信するプロトタイプ |
| ビルドシステム | 維持（CMake + Spack）。C++カーネル部分に限定 |
| ベンチマークスイート | 維持 + **TORAX検証ケースを追加** |

### Phase 1: MVP — 微分可能な静的結合（6ヶ月） — 改訂

| タスク | v1.0からの変更 |
|--------|--------------|
| JAXベースMHDソルバー | **変更**: C++→JAXで実装。JAX-CFDパターンを参考 |
| 微分可能PIC | **変更**: JAX-in-Cellの拡張として2D3V PICを実装 |
| 静的ドメイン結合 + GTL | **変更**: Chapman-Enskog→段階的遷移層（GTL）での結合 |
| End-to-end AD検証 | **新規**: 結合シミュレーション全体を通した勾配伝播の検証 |
| C++カーネル（Boris pusher） | 維持。JAX custom callでの呼び出し |

**新しい検証ケース**: GEM磁気再結合問題に加え、**結合シミュレーション全体の勾配を用いた初期条件最適化**（再結合率を最大化するプラズマパラメータの逆問題）をPhase 1の成功指標に追加。

### Phase 2: 動的結合 + PINO + シンプレクティック補正（9ヶ月） — 改訂

| タスク | v1.0からの変更 |
|--------|--------------|
| AMMC + GTL統合 | **変更**: 3層遷移ゾーンの実装 |
| FNOベースクロージャ | **新規**: Huang et al. (2025) の手法を実装。Vlasovモーメントからの熱フラックス学習 |
| PINO + SympMat補正 | **変更**: DeepONet/FNO + シンプレクティック補正の二段構成 |
| 不確実性定量化 | **新規**: MC Dropout / Deep Ensemble による動的PICフォールバック |
| 転移学習パイプライン | **新規**: 3段階学習（汎用ベース→物理特化→オンライン適応） |
| WarpXデータ取得 | **新規**: WarpX大規模実行データの取得・前処理 |

### Phase 3: 二層最適化型自律進化ループ（6ヶ月） — 改訂

| タスク | v1.0からの変更 |
|--------|--------------|
| Diagnostics Engine | 維持 |
| Bilevel Optimizer | **変更**: Model Critic + Code Synthesizer → LLM（離散提案）+ AD（連続最適化） |
| 信頼度階層型ポリシー | **新規**: L1–L4の4段階自動適用ポリシー |
| MCP-SIM型エージェント統合 | **新規**: 計画-実行-反省-修正サイクルの実装 |
| リグレッションテスト | 維持 + **逆問題ベースの検証を追加**（勾配情報を活用） |

### Phase 4: 核融合プラズマ応用 + エクサスケール（12ヶ月〜） — 改訂

| タスク | v1.0からの変更 |
|--------|--------------|
| 3Dトロイダル形状 | 維持 |
| Kokkosポータビリティ | **新規**: AMD/Intel GPUへのポータビリティ確保 |
| マルチノードスケーリング | **変更**: 4–8 GPU → **数百GPU**（JAX pjit + Kokkos） |
| TORAX統合 | **新規**: コア輸送シミュレータとしてTORAXを検証・統合 |
| ITER/JT-60SAパラメータ | 維持 |

---

## 10. 結論

v1.0の提案は、核融合プラズマシミュレーションの根本的な限界に対する数理的に健全な解答であった。しかし、実装への道には5つの壁が立ちはだかっていた。本稿では、2024–2026年の最新研究を体系的にレビューした結果、以下の結論に到達した：

### ソフトウェア上の最大のブレイクスルーは「微分可能性」である

JAX-in-Cell (2025)、TORAX (2024)、そして微分可能プラズマ物理の体系的実証 (2026) が示すように、**プラズマシミュレーション全体を自動微分可能にする**技術的基盤はすでに存在する。これにより：

1. PINOの学習が事後的データ収集からend-to-end勾配伝播に移行し、**学習効率が飛躍的に向上**する
2. 自律進化ループのパラメータ最適化が勾配降下法で実行可能になり、**探索効率が指数的に改善**する
3. 逆問題への応用が可能になり、実験データとの直接的なフィードバックループが形成される

### 構造保存型ニューラルネットワークがPINOの長時間安定性を解決する

シンプレクティックニューラルネットワーク (Dong et al., 2025; Liang et al., 2025) をPINOの後段補正として組み込むことで、ニューラル演算子の高速性とハミルトン力学の構造保存性を**両立**できる見通しが立った。

### 自律進化ループは二層最適化で現実的になる

LLMの物理的推論の信頼性問題は、SGA (ICML 2024) の二層最適化枠組み — LLMは離散構造の提案、微分可能シミュレータは連続パラメータの最適化 — により大幅に緩和される。MCP-SIM (2026) の反復的自己修正アーキテクチャは、この枠組みの堅牢性をさらに高める。

### エクサスケール既存資産の活用が開発を加速する

WarpX、XGCの実績あるエクサスケールコードを「競合」ではなく「学習データ生成源」として位置づけることで、Phase 0–2の開発を大幅に加速できる。ADIOS2による標準的な接続インターフェースは、追加開発なしで利用可能である。

**本提案の核心的メッセージ**: v1.0で提示した物理的枠組みの実現可能性は、この2年間のソフトウェア技術の進歩により劇的に向上した。特にJAXエコシステムの成熟と構造保存型ニューラルネットワークの実用化は、v1.0執筆時には予見できなかった加速因子である。今後の開発は、これらの新しい道具を最大限に活用する方向に舵を切るべきである。

---

## 11. 参考文献

### v1.0からの継続参照

[1] Markidis, S., & Lapenta, G. (2011). "Multi-scale simulations of plasma with iPIC3D." *Math. Comput. Simul.*, 80(7), 1509-1519.

[2] Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). "Physics-informed neural networks." *J. Comput. Phys.*, 378, 686-707.

[3] Lu, L., Jin, P., & Karniadakis, G. E. (2021). "DeepONet: Learning nonlinear operators." *Nat. Mach. Intell.*, 3, 218-229.

[4] Li, Z., et al. (2021). "Physics-Informed Neural Operator for Learning Partial Differential Equations." arXiv:2111.03794.

### ニューラル演算子・サロゲートモデル（2024–2026）

[5] Gopakumar, V., et al. (2024). "Plasma Surrogate Modelling using Fourier Neural Operators." *Nuclear Fusion*, 64, 056025. arXiv:2311.05967.

[6] Neural Operator Surrogate Models of Plasma Edge Simulations (2025). arXiv:2502.17386.

[7] "AI-driven Physics-Informed Neural Operators for Predictive Modelling of Plasma Turbulence." *Eur. Phys. J. Plus* (2025).

[8] Huang, F., et al. (2025). "FNO-based Closure for Vlasov Moments." (Vlasovソルバー訓練データによるFNOクロージャモデル)

### マルチスケール結合（2024–2025）

[9] Haahr, M., Gudiksen, B., & Nordlund, Å. (2025). "Coupling Particle-in-Cell and Magnetohydrodynamics Methods for Realistic Solar Flare Models." *Astron. Astrophys.* (accepted).

[10] "State of the Art of Gyrokinetic and Hybrid MHD-Kinetic Codes through Non-Linear Benchmarking." *Rev. Mod. Plasma Phys.* (2025).

[11] Allmann-Rahn, F., Lautenbach, S., Deisenhofer, M., & Grauer, R. (2024). "The muphyII Code: Multiphysics Plasma Simulation on Large HPC Systems." *Comput. Phys. Commun.*

### AI駆動型科学的発見（2024–2026）

[12] Park, D., Moon, H., & Ryu, S. (2026). "MCP-SIM: A Self-Correcting Multi-Agent LLM Framework for Language-Based Physics Simulation and Explanation." *npj Artif. Intell.*

[13] Ma, P., et al. (2024). "LLM and Simulation as Bilevel Optimizers: A New Paradigm to Advance Physical Scientific Discovery." *ICML 2024*, PMLR 235:33940-33962. arXiv:2405.09783.

[14] Lu, C., et al. (2025). "The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search." arXiv:2504.08066.

### 微分可能プラズマシミュレーション（2024–2026）

[15] "Differentiable Programming for Plasma Physics: From Diagnostics to Discovery and Design." (2026). arXiv:2603.11231.

[16] "Differentiable Programming for Computational Plasma Physics." (2024). arXiv:2410.11161.

[17] Citrin, J., Goodfellow, I., et al. (2024). "TORAX: A Fast and Differentiable Tokamak Transport Simulator in JAX." arXiv:2406.06718.

[18] Ma, L., et al. (2025). "JAX-in-Cell: A Differentiable Particle-in-Cell Code for Plasma Physics Applications." arXiv:2512.12160.

### 構造保存型ニューラルネットワーク（2024–2025）

[19] Dong, C., et al. (2025). "Symplectic Neural Network and Its Application to Charged Particle Dynamics in Electromagnetic Fields." *Phys. Plasmas*, 32, 103901.

[20] Liang, C., Wen, X., Zhu, Z., et al. (2025). "SPINI: A Structure-Preserving Neural Integrator for Hamiltonian Dynamics and Parametric Perturbation." *Sci. Rep.*

[21] "A Generalized Framework of Neural Networks for Hamiltonian Systems." *J. Comput. Phys.* (2024).

[22] "Approximation of Nearly-Periodic Symplectic Maps via Structure-Preserving Neural Networks (Symplectic Gyroceptron)." *Sci. Rep.* (2023; follow-up 2024–2025).

### GPUおよびエクサスケール計算（2024–2025）

[23] WarpX Team. (2024–2025). WarpX Exascale Computing Platform. Frontier全スケール実行達成。

[24] Marks, T. A., & Gorodetsky, A. A. (2025). "GPU-Accelerated Kinetic Hall Thruster Simulations in WarpX." *J. Electric Propulsion.*

[25] XGC Team / PPPL. (2024–2025). 2024 Kaul Foundation Prize. Frontier上でのダイバータ熱負荷幅予測の実験的検証。

[26] "Porting a Fortran Plasma Simulation to Exascale on AMD GPUs using OpenMP and Kokkos." (2024).

---

*本文書はv1.0の設計提案の技術的課題分析と改訂戦略を示すものであり、各改訂の詳細な実装仕様はPhase 0の技術評価を経て確定される。*
