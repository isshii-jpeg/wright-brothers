# 自律進化型マルチスケール・マルチフィジックス プラズマシミュレーター設計提案書

**Version:** 1.0  
**Date:** 2026-04-01  
**Scope:** ミクロ-マクロ動的結合・AI駆動型自律改善機構を備えた次世代プラズマシミュレーション基盤

---

## 目次

1. [エグゼクティブサマリー](#1-エグゼクティブサマリー)
2. [既存手法の限界と本提案の位置づけ](#2-既存手法の限界と本提案の位置づけ)
3. [アルゴリズム選定](#3-アルゴリズム選定)
4. [システムアーキテクチャ](#4-システムアーキテクチャ)
5. [Auto-research フィードバックループ](#5-auto-research-フィードバックループ)
6. [フェーズ別ロードマップ](#6-フェーズ別ロードマップ)
7. [リスクと緩和策](#7-リスクと緩和策)
8. [参考文献](#8-参考文献)

---

## 1. エグゼクティブサマリー

核融合プラズマの挙動予測において、**電子のジャイロ運動（$\sim 10^{-11}$ s, $\sim 10^{-5}$ m）** から **MHD不安定性の成長（$\sim 10^{-3}$ s, $\sim 1$ m）** までの時空間スケールは $10^8$ 以上の隔たりを持つ。従来のPIC法やMHDソルバーは、このスケール間の動的結合を扱うには根本的な設計限界がある。

本提案では以下の3つの柱により、この壁を突破する：

1. **適応的ミクロ-マクロ結合（Adaptive Micro-Macro Coupling; AMMC）**: 物理的な閾値に基づき、局所的にPIC精度とMHD効率を動的に切り替えるドメイン分解法。
2. **Physics-Informed Neural Operator（PINO）による次元削減**: 高次元Vlasov方程式の解空間をニューラル演算子で近似し、計算コストを $O(N^6) \to O(N^2)$ に削減。
3. **自律進化ループ**: シミュレーション結果からAIが物理モデルの不整合を検出し、モデル修正・コード変更を自動提案する閉ループ機構。

---

## 2. 既存手法の限界と本提案の位置づけ

### 2.1 PIC法の限界

PIC法は粒子の第一原理的追跡により運動論的効果を捉えるが、以下の根本的問題を抱える：

| 課題 | 詳細 |
|------|------|
| **統計ノイズ** | 粒子数 $N_p$ に対し熱揺らぎが $O(1/\sqrt{N_p})$ でしか減衰せず、$N_p \sim 10^{10}$ が必要 |
| **時間ステップ制約** | CFL条件 $\Delta t < \Delta x / c$ により、電磁波伝播速度 $c$ がボトルネック |
| **スケール結合の不在** | マクロ挙動（例：NTM成長）の時間スケールまで粒子追跡を続けるのは計算的に不可能 |

### 2.2 MHD法の限界

| 課題 | 詳細 |
|------|------|
| **運動論的効果の欠落** | 速度分布関数の非Maxwell成分（ビーム、テール）を原理的に記述できない |
| **抵抗性の人為的導入** | 数値抵抗と物理抵抗の分離が困難で、磁気再結合率の定量予測に限界 |
| **クロージャ問題** | 高次モーメントの切断近似が、非平衡プラズマで破綻 |

### 2.3 本提案の差別化

既存のマルチスケール手法（例：XGC, GENE, GTC）は静的なスケール分離を前提とするが、**本提案は物理状態に応じた動的なスケール結合を実現する**。特に磁気再結合やELM（Edge Localized Mode）のように、ミクロ不安定性がマクロ構造を駆動する現象において、この動的結合が決定的な差異を生む。

---

## 3. アルゴリズム選定

### 3.1 適応的ミクロ-マクロ結合（AMMC）

#### 3.1.1 基本思想

計算ドメインを空間的にセルに分割し、各セルにおける**非平衡度指標** $\mathcal{D}$ を定義する：

$$\mathcal{D}(\mathbf{x}, t) = \frac{\| f(\mathbf{x}, \mathbf{v}, t) - f_{\text{Max}}(\mathbf{x}, \mathbf{v}, t) \|_{L^2}}{\| f_{\text{Max}}(\mathbf{x}, \mathbf{v}, t) \|_{L^2}}$$

ここで $f$ は速度分布関数、$f_{\text{Max}}$ は局所Maxwell分布である。

- $\mathcal{D} < \epsilon_{\text{MHD}}$: **MHDソルバー**を適用（流体近似が有効）
- $\epsilon_{\text{MHD}} \leq \mathcal{D} < \epsilon_{\text{kin}}$: **ジャイロ運動論的ソルバー**（$\delta f$ PIC）
- $\mathcal{D} \geq \epsilon_{\text{kin}}$: **フルPICソルバー**（完全運動論的）

閾値 $\epsilon_{\text{MHD}}, \epsilon_{\text{kin}}$ はAIによって動的に校正される（§5参照）。

#### 3.1.2 セル間結合の数学的定式化

MHDセルから運動論セルへの境界条件は、流体モーメントの保存と速度分布関数の整合を同時に要求する。具体的には、MHD側の密度 $n$、流速 $\mathbf{u}$、圧力テンソル $\mathbf{P}$ からChapman-Enskog展開により $f$ の境界値を構成する：

$$f_{\text{boundary}} = f_{\text{Max}}(n, \mathbf{u}, T) \left[ 1 + \sum_{k=1}^{K} \epsilon^k \phi_k(\mathbf{v}) \right]$$

逆方向（運動論→MHD）では、速度空間積分によりモーメントを抽出し、MHD変数に射影する：

$$n = \int f \, d^3v, \quad n\mathbf{u} = \int \mathbf{v} f \, d^3v, \quad \mathbf{P} = m \int (\mathbf{v} - \mathbf{u})(\mathbf{v} - \mathbf{u}) f \, d^3v$$

この双方向結合において**エネルギー・運動量・粒子数の厳密な保存**を保証するために、ラグランジュ未定乗数法による補正を導入する。

#### 3.1.3 適応再分割（Adaptive Mesh Refinement との統合）

AMMCの空間解像度はAMR（Adaptive Mesh Refinement）と連携させる。運動論セルでは自動的に高解像度メッシュが生成され、MHDセルでは粗い格子が使用される。これにより、**計算リソースの動的な再配分**が可能となる。

再分割判定にはWavelet-based error estimatorを使用する：

$$\eta_{\text{cell}} = \max_{|\alpha| \leq p} \| d_\alpha \cdot \psi_\alpha \|_{\infty}$$

ここで $d_\alpha$ はWavelet係数、$\psi_\alpha$ はマザーウェーブレットである。$\eta_{\text{cell}}$ が閾値を超えたセルは細分化され、下回ったセルは粗視化される。

### 3.2 Physics-Informed Neural Operator（PINO）の適用

#### 3.2.1 問題の定式化

Vlasov方程式は6次元位相空間上のPDEである：

$$\frac{\partial f}{\partial t} + \mathbf{v} \cdot \nabla_{\mathbf{x}} f + \frac{q}{m}(\mathbf{E} + \mathbf{v} \times \mathbf{B}) \cdot \nabla_{\mathbf{v}} f = C[f]$$

直接的な離散化は $O(N^6)$ のメモリとフロップを要求し、現実的でない。

#### 3.2.2 PINOによる次元削減戦略

**DeepONet** のBranch-Trunk構造を拡張し、速度分布関数の時間発展演算子を学習する：

$$\mathcal{G}_\theta : f(\cdot, t_n) \mapsto f(\cdot, t_{n+1})$$

ここで $\theta$ はネットワークパラメータである。損失関数には以下を組み込む：

$$\mathcal{L} = \underbrace{\mathcal{L}_{\text{data}}}_{\text{PICデータとの整合}} + \lambda_1 \underbrace{\mathcal{L}_{\text{Vlasov}}}_{\text{Vlasov方程式残差}} + \lambda_2 \underbrace{\mathcal{L}_{\text{conservation}}}_{\text{保存則}} + \lambda_3 \underbrace{\mathcal{L}_{\text{entropy}}}_{\text{Hの定理}}$$

各項の詳細：

- **$\mathcal{L}_{\text{Vlasov}}$**: Vlasov方程式の残差のcollocation pointにおけるMSE
  $$\mathcal{L}_{\text{Vlasov}} = \frac{1}{N_c} \sum_{i=1}^{N_c} \left| \frac{\partial f_\theta}{\partial t} + \mathbf{v} \cdot \nabla_{\mathbf{x}} f_\theta + \frac{q}{m}(\mathbf{E} + \mathbf{v} \times \mathbf{B}) \cdot \nabla_{\mathbf{v}} f_\theta - C[f_\theta] \right|^2$$

- **$\mathcal{L}_{\text{conservation}}$**: 質量・運動量・エネルギー保存の違反ペナルティ
  $$\mathcal{L}_{\text{conservation}} = \left| \frac{d}{dt} \int f_\theta \, d^3x \, d^3v \right|^2 + \left| \frac{d}{dt} \int m\mathbf{v} f_\theta \, d^3x \, d^3v \right|^2 + \cdots$$

- **$\mathcal{L}_{\text{entropy}}$**: ボルツマンのHの定理（エントロピー非減少）の制約
  $$\mathcal{L}_{\text{entropy}} = \text{ReLU}\left( -\frac{d}{dt} \int f_\theta \ln f_\theta \, d^3x \, d^3v \right)$$

#### 3.2.3 適用モジュール

PINOを適用する場面と適用しない場面を明確に分ける：

| モジュール | PINO適用 | 理由 |
|-----------|---------|------|
| 速度分布関数の時間発展 | **Yes** | 6次元空間の直接離散化回避。最大の計算コスト削減効果 |
| 衝突演算子 $C[f]$ | **Yes** | Fokker-Planck衝突積分の高速近似。Rosenbluthポテンシャルの計算を代替 |
| 電磁場ソルバー | **No** | Maxwell方程式は3+1次元で既に効率的なFDTD/スペクトル法が存在 |
| MHD方程式系 | **No** | 十分に成熟した高効率ソルバー（例：HLLC Riemann solver）が利用可能 |
| クロージャモデル | **Yes** | MHDの高次モーメント切断を運動論的データから学習し動的に補正 |
| 磁気再結合のサブグリッドモデル | **Yes** | MHDスケールの格子では分解できない電子散逸領域の効果をサロゲートモデル化 |

#### 3.2.4 オンライン学習とオフライン学習の棲み分け

- **オフライン学習**: 高精度PICシミュレーション（既存コード: VPIC, OSIRIS等）の結果からベースモデルを事前学習。数百GPU時間を想定。
- **オンライン学習**: シミュレーション実行中にPINO予測と局所PIC検証の差異からモデルを微調整。勾配は数十ステップ分蓄積してからバッチ更新し、計算オーバーヘッドを < 5% に抑制。

### 3.3 時間積分スキーム

マルチスケールの時間発展には**IMEX（Implicit-Explicit）法**を採用する：

$$\frac{\mathbf{U}^{n+1} - \mathbf{U}^n}{\Delta t} = \underbrace{F_{\text{fast}}(\mathbf{U}^{n+1})}_{\text{implicit}} + \underbrace{F_{\text{slow}}(\mathbf{U}^n)}_{\text{explicit}}$$

- **Implicit部**: 電子プラズマ振動（$\omega_{pe} \sim 10^{11}$ rad/s）、電磁波伝播を暗黙的に処理 → CFL制約からの解放
- **Explicit部**: イオンスケールの運動、MHD波動を陽的に時間積分

これにより、時間ステップを電子スケール（$\sim 10^{-12}$ s）からイオンスケール（$\sim 10^{-8}$ s）へ $10^4$ 倍拡大できる。

---

## 4. システムアーキテクチャ

### 4.1 ハイブリッド言語構成

```
┌─────────────────────────────────────────────────────────┐
│                  Orchestration Layer                     │
│                 Python (asyncio + Ray)                   │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ Workflow │  │ AI Training  │  │  Auto-research    │  │
│  │ Control  │  │ (PyTorch)    │  │  Feedback Loop    │  │
│  └────┬─────┘  └──────┬───────┘  └────────┬──────────┘  │
│       │               │                   │              │
├───────┼───────────────┼───────────────────┼──────────────┤
│       │      Compute Engine Layer         │              │
│       ▼               ▼                   ▼              │
│  ┌─────────────────────────────────────────────────┐     │
│  │              Julia (Glue Layer)                  │     │
│  │  - AMMC domain decomposition logic              │     │
│  │  - Adaptive threshold calibration               │     │
│  │  - In-situ diagnostics & visualization          │     │
│  └────────────┬───────────────────┬────────────────┘     │
│               │                   │                      │
│  ┌────────────▼────────┐  ┌──────▼──────────────┐       │
│  │   C++ / CUDA Core   │  │  PINO Inference     │       │
│  │  - PIC pusher       │  │  (TensorRT / ONNX)  │       │
│  │  - Field solver     │  │  - Vlasov surrogate │       │
│  │  - MHD integrator   │  │  - Closure model    │       │
│  │  - Particle deposit │  │  - Collision approx │       │
│  └─────────────────────┘  └─────────────────────┘       │
│                                                          │
├──────────────────────────────────────────────────────────┤
│                   Data / Memory Layer                     │
│  ┌──────────────────────────────────────────────────┐    │
│  │  Apache Arrow (zero-copy IPC)                    │    │
│  │  + HDF5 (checkpoint I/O)                         │    │
│  │  + Redis (real-time metrics stream)              │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

### 4.2 各層の役割と言語選択の根拠

| 層 | 言語 | 根拠 |
|----|------|------|
| **Orchestration** | Python | Ray によるタスクスケジューリング、PyTorch によるAI学習、豊富なエコシステム |
| **Glue / Logic** | Julia | 科学計算のパフォーマンスとPythonに近い記述性の両立。Multiple dispatch によるAMMCの物理モデル切替が自然に記述可能 |
| **Compute Core** | C++ / CUDA | レイテンシクリティカルなカーネル（粒子プッシャー、場ソルバー）。メモリレイアウトの完全制御 |
| **AI Inference** | TensorRT | 学習済みPINOのGPU推論を最適化。FP16/INT8量子化による高スループット |

### 4.3 Threadripper最適化：メモリ帯域を活かすデータ構造

AMD Threadripper（例：7995WX, 96コア, 8チャネルDDR5）の特性：
- **メモリ帯域**: 最大 ~307 GB/s（8ch DDR5-4800）
- **L3キャッシュ**: 384 MB（CCD×12）
- **NUMAトポロジ**: 4 NUMAノード（各24コア）

#### 4.3.1 粒子データのStructure of Arrays (SoA) レイアウト

従来のAoS（Array of Structures）:
```cpp
// AoS: キャッシュライン効率が悪い
struct Particle { double x, y, z, vx, vy, vz, q, m; };  // 64 bytes
std::vector<Particle> particles;  // 1粒子 = 1キャッシュライン
```

本提案のSoA:
```cpp
// SoA: SIMD (AVX-512) に最適。1キャッシュラインで8粒子のx座標を処理
struct ParticleArray {
    alignas(64) double* x;   // x[0..N-1]
    alignas(64) double* y;
    alignas(64) double* z;
    alignas(64) double* vx;
    alignas(64) double* vy;
    alignas(64) double* vz;
    alignas(64) double* q;
    alignas(64) double* m;
    size_t count;
};
```

粒子プッシャー（Boris法）のカーネルでは、$\mathbf{v}$ の更新時に `vx, vy, vz` を連続アクセスする。SoAレイアウトにより、AVX-512で8粒子を同時処理でき、メモリ帯域利用率を **AoS比 3〜4倍** に改善できる。

#### 4.3.2 NUMA-aware メモリ配置

```
NUMA Node 0 (Core 0-23)     NUMA Node 1 (Core 24-47)
┌──────────────────────┐    ┌──────────────────────┐
│ Spatial Domain 0     │    │ Spatial Domain 1     │
│ - Local particles    │    │ - Local particles    │
│ - Local field grid   │    │ - Local field grid   │
│ - Ghost zone buffer  │◄──►│ - Ghost zone buffer  │
└──────────────────────┘    └──────────────────────┘

NUMA Node 2 (Core 48-71)    NUMA Node 3 (Core 72-95)
┌──────────────────────┐    ┌──────────────────────┐
│ Spatial Domain 2     │    │ Spatial Domain 3     │
│ ...                  │    │ ...                  │
└──────────────────────┘    └──────────────────────┘
```

- 空間ドメインをNUMAノードに1:1マッピング
- `numactl --membind` + `pthread_setaffinity_np` で粒子データと場データをローカルメモリに固定
- ゴーストゾーン交換は `memcpy` ではなく**RDMA-style のnon-blocking copy**（`hwloc` + カスタムアロケータ）

#### 4.3.3 GPU（CUDA）オフロード戦略

```
Threadripper (Host)                    GPU (e.g., RTX 4090 / A100)
┌────────────────────┐                ┌──────────────────────────┐
│ AMMC制御ロジック    │                │ Particle Pusher Kernel   │
│ AMR再分割判定      │   PCIe 5.0    │ Field Solver (FFT-based) │
│ I/O・チェックポイント│◄════════════►│ PINO Inference           │
│ AI学習(PyTorch)    │  64 GB/s      │ Particle Sorting         │
└────────────────────┘                └──────────────────────────┘
```

**転送コスト最小化の原則:**
- 粒子データは基本的にGPUメモリに常駐。ホストへの転送は診断出力時のみ。
- 場データは各タイムステップでGPU→Host転送が発生するが、サイズが粒子データの $O(1/N_{\text{ppc}})$ 倍（$N_{\text{ppc}}$: セルあたり粒子数）であるため許容範囲。
- PINO推論はGPU上で完結。学習時の勾配計算もGPUで実行し、パラメータ更新のみHostで管理。
- **CUDA Unified Memory** は使用しない（暗黙的なページマイグレーションによる性能低下を回避）。明示的な `cudaMemcpyAsync` + CUDA Stream による転送/計算のオーバーラップを徹底する。

### 4.4 並列計算アーキテクチャ詳細

#### 4.4.1 ハイブリッド並列化モデル

```
Level 1: MPI (ノード間 / NUMAノード間)
  └─ Level 2: OpenMP (NUMAノード内コア並列)
       └─ Level 3: CUDA (GPU内スレッド並列)
            └─ Level 4: AVX-512 (CPU SIMD)
```

- **Level 1 (MPI)**: 空間ドメイン分解。各MPI rankが1つのNUMAノード（24コア + GPUスライス）を担当。
- **Level 2 (OpenMP)**: MPI rank内の粒子ループ並列化。動的スケジューリング（`schedule(dynamic, 256)`）で粒子数の不均衡に対応。
- **Level 3 (CUDA)**: 粒子プッシャーは1スレッド1粒子。場ソルバーはcuFFTベースのスペクトル法。
- **Level 4 (AVX-512)**: CPU上のMHDソルバーにおけるRiemann solver のSIMD化。

#### 4.4.2 負荷分散

AMMCでは計算負荷がドメイン毎に大きく異なる（PICセルはMHDセルの $\sim 100$倍重い）。**Hilbert曲線ベースの空間充填曲線分解**を採用し、計算重みを考慮した動的再分割を行う：

$$W_{\text{cell}} = \begin{cases} w_{\text{MHD}} \cdot N_{\text{grid}} & \text{(MHD cell)} \\ w_{\text{PIC}} \cdot N_{\text{particles}} & \text{(PIC cell)} \\ w_{\text{PINO}} \cdot N_{\text{inference}} & \text{(PINO cell)} \end{cases}$$

再分割は $N_{\text{rebalance}}$ ステップ毎に実行し、Hilbert曲線上で各MPI rankの総重み $\sum W$ を均等化する。

---

## 5. Auto-research フィードバックループ

### 5.1 全体アーキテクチャ

```
┌─────────────────────────────────────────────────────┐
│                 Simulation Core                      │
│         (AMMC + PINO + Field Solver)                │
└───────────────┬─────────────────────────────────────┘
                │ (1) Raw simulation data
                ▼
┌─────────────────────────────────────────────────────┐
│              Diagnostics Engine                      │
│  - Conservation law violation monitor               │
│  - Spectral analysis (instability detection)        │
│  - Statistical divergence from PIC ground truth     │
└───────────────┬─────────────────────────────────────┘
                │ (2) Anomaly reports + metrics
                ▼
┌─────────────────────────────────────────────────────┐
│            Model Critic (LLM-based)                  │
│  - Analyzes anomaly patterns                        │
│  - Cross-references plasma physics literature       │
│  - Proposes model modifications in natural language  │
└───────────────┬─────────────────────────────────────┘
                │ (3) Modification proposals
                ▼
┌─────────────────────────────────────────────────────┐
│            Code Synthesizer                          │
│  - Translates proposals to code patches             │
│  - Runs unit tests + conservation law checks        │
│  - Submits PR for human review                      │
└───────────────┬─────────────────────────────────────┘
                │ (4) Validated code changes
                ▼
┌─────────────────────────────────────────────────────┐
│            Regression Test Suite                      │
│  - Known analytic solutions (Landau damping, etc.)  │
│  - Energy conservation to machine precision         │
│  - Performance benchmarks (no regression)           │
└───────────────┬─────────────────────────────────────┘
                │ (5) Pass/Fail
                ▼
            ┌───┴───┐
            │ Human │ ──── Approve/Reject
            │Review │
            └───┬───┘
                │ (6) Approved changes
                ▼
         Simulation Core (updated)
```

### 5.2 Diagnostics Engine：異常検知メトリクス

以下のメトリクスを常時監視し、物理モデルの改善が必要な箇所を特定する：

#### 5.2.1 保存則違反度

$$\epsilon_{\text{energy}}(t) = \frac{|E_{\text{total}}(t) - E_{\text{total}}(0)|}{E_{\text{total}}(0)}$$

$\epsilon_{\text{energy}} > 10^{-6}$（倍精度限界の$10^3$倍）で警告を発出。

#### 5.2.2 PINOとPIC参照解の統計的乖離

定期的に局所領域でフルPIC計算を実行し、PINOの予測と比較する：

$$D_{\text{KL}}(f_{\text{PIC}} \| f_{\text{PINO}}) = \int f_{\text{PIC}} \ln \frac{f_{\text{PIC}}}{f_{\text{PINO}}} \, d^3v$$

$D_{\text{KL}}$ が閾値を超えた領域は、PINOモデルの再学習候補としてフラグされる。

#### 5.2.3 物理的不整合スペクトル

線形MHD安定性理論の予測する成長率 $\gamma_{\text{theory}}$ と、シミュレーションで観測される成長率 $\gamma_{\text{sim}}$ の比較：

$$R_{\gamma} = \frac{\gamma_{\text{sim}} - \gamma_{\text{theory}}}{\gamma_{\text{theory}}}$$

$|R_{\gamma}| > 0.1$ の不安定性モードが検出された場合、モデルの改善提案をトリガーする。

### 5.3 Model Critic：LLMベースの物理モデル分析

Diagnostics Engineからの異常レポートを受け取り、以下のプロンプトテンプレートでLLM（Claude API）に分析を依頼する：

```
You are a plasma physicist analyzing simulation anomalies.

## Anomaly Report
- Type: {anomaly_type}
- Location: {spatial_region}
- Magnitude: {metric_value}
- Time window: {t_start} to {t_end}
- Active physics models: {model_list}

## Context
- Plasma parameters: β={beta}, S={lundquist}, ν*={collisionality}
- Geometry: {geometry_description}

## Task
1. Identify the most likely physical mechanism causing this anomaly.
2. Propose specific modifications to the simulation model.
3. Estimate the expected impact on simulation accuracy.
4. Cite relevant literature if applicable.
```

### 5.4 安全性保証

自律進化ループには以下の安全弁を設ける：

1. **保存則ハードリミット**: いかなる修正も、エネルギー・運動量・粒子数保存を $10^{-10}$ 以上違反する場合は自動リジェクト。
2. **漸進的適用**: コード変更は常に限定的な空間領域で先行テストし、全領域への展開前にリグレッションテストを通過させる。
3. **人間のゲートキーピング**: 物理モデルの構造的変更（例：新しい項の追加、方程式の変更）は必ず人間の承認を経る。パラメータの微調整のみ自動適用を許可。
4. **ロールバック機構**: 全変更はGit管理され、性能劣化が検出された場合に即座にロールバック可能。

---

## 6. フェーズ別ロードマップ

### Phase 0: 基盤整備（3ヶ月）

**目標**: 開発環境の構築と基本コンポーネントの選定

| タスク | 詳細 | 成果物 |
|--------|------|--------|
| ビルドシステム | CMake + Spack による依存管理 | 再現可能なビルド環境 |
| CI/CD | GitHub Actions + self-hosted runner (Threadripper) | 自動テスト・ベンチマークパイプライン |
| ベンチマークスイート | Landau減衰、二流体不安定性、GEM磁気再結合 | 検証用参照解データセット |
| PIC基盤 | 既存OSSコード（例: WarpX）のforkまたはコア抽出 | 動作する2D3V PICコード |

### Phase 1: MVP — 静的結合（6ヶ月）

**目標**: PICとMHDの静的（手動）結合が動作するプロトタイプ

| タスク | 詳細 |
|--------|------|
| MHDソルバー実装 | Ideal MHD, HLLC Riemann solver, 2D structured grid |
| 静的ドメイン結合 | 手動で指定した境界でPIC↔MHD変数を受け渡し |
| 保存則検証 | 結合境界でのエネルギー・粒子フラックスの保存を確認 |
| CUDA移植 | 粒子プッシャー + 場ソルバーのGPUカーネル化 |

**検証ケース**: GEM磁気再結合問題。再結合領域をPIC、周辺をMHDで計算し、再結合率がフルPICの結果を ±10% 以内で再現することを確認。

### Phase 2: 動的結合 + PINO導入（9ヶ月）

**目標**: AMMCの動的切り替えとPINOの初期モデル

| タスク | 詳細 |
|--------|------|
| AMMC実装 | 非平衡度指標 $\mathcal{D}$ の実装、動的セル再分類 |
| AMR統合 | Wavelet-based error estimator + p4estライブラリ連携 |
| PINOベースモデル | 1D Vlasov-Poisson問題でのDeepONet学習・検証 |
| Hilbert曲線負荷分散 | 重み付き空間充填曲線分解の実装 |
| Julia glue layer | AMMCロジックのJulia実装、C++/CUDAコアとのFFI |

**検証ケース**: Kelvin-Helmholtz不安定性の非線形発展。運動論的効果が重要になる渦巻き込み領域が自動的にPICに切り替わることを確認。

### Phase 3: Auto-research ループ（6ヶ月）

**目標**: 自律改善機構の実装と初期動作確認

| タスク | 詳細 |
|--------|------|
| Diagnostics Engine | 保存則監視、KLダイバージェンス計算、不安定性成長率比較 |
| Model Critic | LLM APIとの統合、プロンプトテンプレート設計 |
| Code Synthesizer | 提案からコードパッチを生成、テスト自動実行 |
| リグレッションテスト | 解析解ベンチマーク、保存則テスト、性能テスト |

**検証ケース**: 意図的にクロージャモデルに欠陥を導入し、Auto-researchループが (a) 問題を検出し、(b) 正しい改善を提案し、(c) 提案が人間のレビュー後に適用され、(d) 精度が回復することを確認。

### Phase 4: 核融合プラズマ応用（12ヶ月〜）

**目標**: 実用的なトカマクプラズマ安定性解析

| タスク | 詳細 |
|--------|------|
| 3Dトロイダル形状対応 | 曲線座標系（磁気座標）への拡張 |
| 抵抗性壁モード（RWM）解析 | 壁との電磁結合を含むMHD安定性 |
| ELMサイクル模擬 | ペデスタル圧力勾配駆動のELM crash → 回復 → 再crash |
| ITER/JT-60SAパラメータ | 実機相当のパラメータでの安定性マップ作成 |
| マルチGPUスケーリング | NCCL通信によるマルチGPU対応（4〜8 GPU） |

---

## 7. リスクと緩和策

| リスク | 影響度 | 緩和策 |
|--------|--------|--------|
| PINO予測精度が不十分 | 高 | PICフォールバック機構を常に維持。PINOは加速手段であり、精度が不足する領域では自動的にPICに切り替え |
| AMMC境界での非物理的アーティファクト | 高 | 保存則の厳密な強制（ラグランジュ乗数法）、境界にバッファゾーンを設け漸進的に遷移 |
| Auto-researchによる誤った物理モデル変更 | 中 | 人間ゲートキーピング必須。パラメータ変更のみ自動許可、方程式構造変更は人間承認 |
| GPU メモリ不足（大規模3D問題） | 中 | 粒子のout-of-core管理、PINO推論のバッチサイズ動的調整、マルチGPU分散 |
| 言語間IPC のレイテンシ | 低 | Apache Arrow zero-copy IPC、共有メモリベース通信。メインループ内のIPC呼出回数を最小化 |

---

## 8. 参考文献

1. Markidis, S., & Lapenta, G. (2011). "Multi-scale simulations of plasma with iPIC3D." *Mathematics and Computers in Simulation*, 80(7), 1509-1519.
2. Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). "Physics-informed neural networks." *Journal of Computational Physics*, 378, 686-707.
3. Lu, L., Jin, P., & Karniadakis, G. E. (2021). "DeepONet: Learning nonlinear operators." *Nature Machine Intelligence*, 3, 218-229.
4. Li, Z., et al. (2021). "Physics-Informed Neural Operator for Learning Partial Differential Equations." *ACM/JMS Journal of Data Science* (preprint arXiv:2111.03794).
5. Tóth, G., et al. (2012). "Adaptive numerical algorithms in space weather modeling." *Journal of Computational Physics*, 231(3), 870-903.
6. Vay, J.-L., et al. (2018). "Warp-X: A new exascale computing platform for beam–plasma simulations." *Nuclear Instruments and Methods in Physics Research A*, 909, 476-479.
7. Birdsall, C. K., & Langdon, A. B. (2004). *Plasma Physics via Computer Simulation*. CRC Press.
8. Bowers, K. J., et al. (2008). "Ultrahigh performance three-dimensional electromagnetic relativistic kinetic plasma simulation." *Physics of Plasmas*, 15(5), 055703.

---

*本提案書は技術的方向性を示すものであり、実装の詳細は各フェーズの設計レビューにおいて精緻化される。*
