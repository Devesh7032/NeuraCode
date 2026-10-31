import React, { useState, useEffect, useRef } from "react";
import { 
  Play, Pause, SkipForward, SkipBack, RotateCcw, 
  Loader2, Info, Eye
} from "lucide-react";

interface VisualizationEngineProps {
  challenge: {
    id: string;
    title: string;
    slug: string;
    visualization_type?: string;
    visualization_config?: string;
  };
  visualizationData: any;
  onRunExperiment: (customInputs: any) => void;
  running: boolean;
}

export const VisualizationEngine: React.FC<VisualizationEngineProps> = ({
  challenge,
  visualizationData,
  onRunExperiment,
  running
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1); // 0.5, 1, 2
  const timerRef = useRef<any>(null);

  // Reset step on new visualization data
  useEffect(() => {
    setCurrentStep(0);
    setIsPlaying(false);
  }, [visualizationData]);

  // Handle iteration steps playback
  useEffect(() => {
    if (isPlaying && visualizationData?.steps && visualizationData.steps.length > 0) {
      const interval = (1000 / playbackSpeed);
      timerRef.current = setInterval(() => {
        setCurrentStep((prev) => {
          if (prev >= visualizationData.steps.length - 1) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, interval);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPlaying, visualizationData, playbackSpeed]);

  if (!challenge.visualization_type) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-500 font-mono text-xs p-6 text-center">
        <Info className="w-6 h-6 mb-2 text-slate-600" />
        No visualization configuration is defined for this challenge.
      </div>
    );
  }

  if (!visualizationData) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-400 font-mono text-xs p-6 text-center select-none bg-dark-deep/30 border border-dashed border-dark-border rounded-lg m-4">
        <Eye className="w-8 h-8 mb-3 text-slate-500 animate-pulse" />
        <h4 className="font-bold text-slate-300 mb-1 text-sm">Visual Experiment Idle</h4>
        <p className="max-w-xs text-slate-500 leading-relaxed">
          Run your solution first to generate real data-driven trace representations.
        </p>
      </div>
    );
  }

  const type = visualizationData.type || challenge.visualization_type;

  // Custom Controls and Sliders based on Visualizer Type
  return (
    <div className="flex flex-col h-full bg-dark text-slate-300 select-text">
      
      {/* Visual Workspace Canvas */}
      <div className="flex-1 min-h-0 overflow-y-auto p-4 space-y-4">
        
        {/* Render appropriate Visual Graph */}
        {type === "FUNCTION" && (
          <FunctionVisualizer 
            data={visualizationData} 
            slug={challenge.slug}
            onUpdate={onRunExperiment} 
            running={running} 
          />
        )}

        {type === "BAR_CHART" && (
          <SoftmaxVisualizer 
            data={visualizationData} 
            onUpdate={onRunExperiment} 
            running={running} 
          />
        )}

        {type === "VECTOR" && (
          <VectorVisualizer 
            data={visualizationData} 
            onUpdate={onRunExperiment} 
            running={running} 
          />
        )}

        {type === "MATRIX_MULTIPLICATION" && (
          <MatrixVisualizer data={visualizationData} />
        )}

        {type === "GRADIENT_DESCENT" && (
          <GradientDescentVisualizer 
            data={visualizationData} 
            currentStep={currentStep} 
            setCurrentStep={setCurrentStep}
            isPlaying={isPlaying}
            setIsPlaying={setIsPlaying}
            playbackSpeed={playbackSpeed}
            setPlaybackSpeed={setPlaybackSpeed}
            onUpdate={onRunExperiment}
            running={running}
          />
        )}

        {type === "LINEAR_REGRESSION" && (
          <LinearRegressionVisualizer 
            data={visualizationData} 
            onUpdate={onRunExperiment}
            running={running}
          />
        )}

        {type === "K_MEANS" && (
          <KMeansVisualizer data={visualizationData} />
        )}

        {type === "PCA" && (
          <PcaVisualizer data={visualizationData} />
        )}

        {type === "DENSE_LAYER" && (
          <DenseLayerVisualizer data={visualizationData} />
        )}

        {type === "NEURAL_NETWORK" && (
          <NeuralNetworkVisualizer data={visualizationData} />
        )}

        {type === "SCALED_DOT_PRODUCT" && (
          <ScaledDotProductVisualizer data={visualizationData} />
        )}

        {type === "ATTENTION_SCORES" && (
          <AttentionScoresVisualizer data={visualizationData} />
        )}

        {type === "SELF_ATTENTION" && (
          <SelfAttentionVisualizer data={visualizationData} />
        )}

        {type === "EMBEDDING_SIMILARITY" && (
          <EmbeddingSimilarityVisualizer data={visualizationData} />
        )}

      </div>
    </div>
  );
};

// ==========================================
// 1. FUNCTION VISUALIZER (Sigmoid, ReLU, Tanh)
// ==========================================
interface FunctionVisualizerProps {
  data: { x: number[]; y: number[]; custom_x: number; custom_y: number };
  slug: string;
  onUpdate: (inputs: any) => void;
  running: boolean;
}
const FunctionVisualizer: React.FC<FunctionVisualizerProps> = ({ data, slug, onUpdate, running }) => {
  const [valZ, setValZ] = useState(data.custom_x);

  const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseFloat(e.target.value);
    setValZ(value);
  };

  const handleApply = () => {
    onUpdate({ z: valZ });
  };

  // Convert mathematical coordinate lists to SVG path
  // range x: [-10, 10], y: [-2, 2]
  const width = 300;
  const height = 150;
  const padding = 20;

  const mapX = (x: number) => padding + ((x + 10) / 20) * (width - 2 * padding);
  const mapY = (y: number) => height - padding - ((y + 2) / 4) * (height - 2 * padding);

  let pathPoints = "";
  if (data.x && data.y) {
    pathPoints = data.x
      .map((xVal, idx) => `${mapX(xVal)},${mapY(data.y[idx])}`)
      .join(" ");
  }

  return (
    <div className="bg-dark-deep/40 border border-dark-border rounded-lg p-4 space-y-4">
      <div className="flex justify-between items-center">
        <h4 className="text-xs font-bold text-slate-300 font-mono">📈 Mathematical Function Trace</h4>
        <span className="text-[10px] bg-dark-card border border-dark-border px-2 py-0.5 rounded font-mono text-slate-400">
          Slug: {slug}
        </span>
      </div>

      <div className="flex justify-center bg-dark-deep rounded border border-dark-border/40 py-4 relative">
        <svg width={width} height={height} className="overflow-visible font-mono text-[9px] text-slate-600">
          {/* Axis lines */}
          <line x1={padding} y1={mapY(0)} x2={width - padding} y2={mapY(0)} stroke="#1C2922" strokeWidth={1} />
          <line x1={mapX(0)} y1={padding} x2={mapX(0)} y2={height - padding} stroke="#1C2922" strokeWidth={1} />

          {/* Labels */}
          <text x={width - padding + 5} y={mapY(0) + 3} fill="#8B958E">z</text>
          <text x={mapX(0) - 12} y={padding - 5} fill="#8B958E">y</text>
          
          <text x={mapX(-10)} y={mapY(0) + 12} textAnchor="middle" fill="#8B958E">-10</text>
          <text x={mapX(10)} y={mapY(0) + 12} textAnchor="middle" fill="#8B958E">10</text>
          <text x={mapX(0) - 10} y={mapY(1.0) + 3} textAnchor="end" fill="#8B958E">1.0</text>
          <text x={mapX(0) - 10} y={mapY(-1.0) + 3} textAnchor="end" fill="#8B958E">-1.0</text>

          {/* Function Plot */}
          {pathPoints && (
            <polyline
              fill="none"
              stroke="#12DFFF"
              strokeWidth={2}
              points={pathPoints}
            />
          )}

          {/* Active Slider coordinate */}
          {data.custom_x !== undefined && data.custom_y !== undefined && (
            <circle
              cx={mapX(data.custom_x)}
              cy={mapY(data.custom_y)}
              r={5}
              fill="#FF4FA3"
              className="animate-pulse"
            />
          )}
        </svg>

        {/* Floating coordinates indicator */}
        <div className="absolute right-3 top-3 text-[10px] font-mono bg-dark-card border border-dark-border px-2 py-1 rounded text-slate-400">
          <div>z: <span className="text-[#12DFFF] font-bold">{data.custom_x?.toFixed(2)}</span></div>
          <div>output: <span className="text-[#FF4FA3] font-bold">{data.custom_y?.toFixed(4)}</span></div>
        </div>
      </div>

      <div className="space-y-2">
        <label className="text-[11px] text-slate-400 font-mono flex justify-between">
          <span>Modify slider input (z-parameter):</span>
          <span className="text-white font-bold">{valZ.toFixed(1)}</span>
        </label>
        <div className="flex gap-3">
          <input
            type="range"
            min="-10.0"
            max="10.0"
            step="0.5"
            value={valZ}
            onChange={handleSliderChange}
            className="flex-1 accent-[#12DFFF] bg-dark-card border border-dark-border rounded h-2 outline-none cursor-pointer mt-1.5"
          />
          <button
            onClick={handleApply}
            disabled={running}
            className="bg-brand hover:bg-brand-dark text-dark-deep font-bold px-3 py-1 text-xs rounded transition-all flex items-center gap-1 shrink-0 font-mono disabled:opacity-40"
          >
            {running ? <Loader2 className="w-3 h-3 animate-spin" /> : null} Apply
          </button>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 2. SOFTMAX VISUALIZER (Bar chart)
// ==========================================
interface SoftmaxVisualizerProps {
  data: { logits: number[]; probabilities: number[] };
  onUpdate: (inputs: any) => void;
  running: boolean;
}
const SoftmaxVisualizer: React.FC<SoftmaxVisualizerProps> = ({ data, onUpdate, running }) => {
  const [l0, setL0] = useState(data.logits[0] || 1.0);
  const [l1, setL1] = useState(data.logits[1] || 2.0);
  const [l2, setL2] = useState(data.logits[2] || 3.0);

  const handleUpdate = () => {
    onUpdate({ logits: [l0, l1, l2] });
  };

  return (
    <div className="bg-dark-deep/40 border border-dark-border rounded-lg p-4 space-y-4 font-mono">
      <h4 className="text-xs font-bold text-slate-300">📊 Softmax Probabilities Graph</h4>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Logit Inputs */}
        <div className="space-y-3 bg-dark-card/40 border border-dark-border rounded p-3 text-xs">
          <h5 className="font-bold text-slate-400 text-[10px] uppercase">Input Logits (Raw Values)</h5>
          
          <div className="space-y-2">
            <label className="flex justify-between text-[11px]">
              <span>Logit #1</span>
              <span className="text-[#12DFFF] font-bold">{l0.toFixed(1)}</span>
            </label>
            <input 
              type="range" min="-5" max="5" step="0.5" value={l0} 
              onChange={e => setL0(parseFloat(e.target.value))} 
              className="w-full accent-[#12DFFF]"
            />
          </div>

          <div className="space-y-2">
            <label className="flex justify-between text-[11px]">
              <span>Logit #2</span>
              <span className="text-[#12DFFF] font-bold">{l1.toFixed(1)}</span>
            </label>
            <input 
              type="range" min="-5" max="5" step="0.5" value={l1} 
              onChange={e => setL1(parseFloat(e.target.value))} 
              className="w-full accent-[#12DFFF]"
            />
          </div>

          <div className="space-y-2">
            <label className="flex justify-between text-[11px]">
              <span>Logit #3</span>
              <span className="text-[#12DFFF] font-bold">{l2.toFixed(1)}</span>
            </label>
            <input 
              type="range" min="-5" max="5" step="0.5" value={l2} 
              onChange={e => setL2(parseFloat(e.target.value))} 
              className="w-full accent-[#12DFFF]"
            />
          </div>

          <button
            onClick={handleUpdate}
            disabled={running}
            className="w-full bg-[#12DFFF]/10 hover:bg-[#12DFFF] text-[#12DFFF] hover:text-dark-deep border border-[#12DFFF]/30 font-bold py-1.5 rounded transition-all text-xs flex justify-center items-center gap-1"
          >
            {running && <Loader2 className="w-3.5 h-3.5 animate-spin" />} Recalculate Softmax
          </button>
        </div>

        {/* Probability Outputs */}
        <div className="space-y-3 bg-dark-card/40 border border-dark-border rounded p-3 text-xs flex flex-col justify-between">
          <div>
            <h5 className="font-bold text-slate-400 text-[10px] uppercase mb-3">Output Probabilities (Sum to 1.0)</h5>
            <div className="space-y-4">
              {data.probabilities.map((prob, idx) => (
                <div key={idx} className="space-y-1.5">
                  <div className="flex justify-between text-[10px]">
                    <span>Class {idx + 1}</span>
                    <span className="text-brand font-bold">{(prob * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-dark-deep rounded-full h-2 overflow-hidden border border-dark-border/60">
                    <div 
                      className="bg-brand h-full rounded-full transition-all duration-300"
                      style={{ width: `${prob * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div className="text-[10px] text-slate-500 border-t border-dark-border/40 pt-2 leading-relaxed">
            Formula: S(z)_i = e^(z_i) / sum(e^(z_j))
          </div>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 3. VECTOR VISUALIZER (2D Coordinates)
// ==========================================
interface VectorVisualizerProps {
  data: { original_vector: number[]; normalized_vector: number[]; magnitude: number };
  onUpdate: (inputs: any) => void;
  running: boolean;
}
const VectorVisualizer: React.FC<VectorVisualizerProps> = ({ data, onUpdate, running }) => {
  const [x, setX] = useState(data.original_vector[0] || 3.0);
  const [y, setY] = useState(data.original_vector[1] || 4.0);

  const handleUpdate = () => {
    onUpdate({ vector: [x, y] });
  };

  const width = 200;
  const height = 200;
  const center = 100;
  const scale = 15; // 1 unit = 15px

  const mapX = (val: number) => center + val * scale;
  const mapY = (val: number) => center - val * scale; // invert Y for Cartesian

  return (
    <div className="bg-dark-deep/40 border border-dark-border rounded-lg p-4 space-y-4 font-mono text-xs">
      <h4 className="text-xs font-bold text-slate-300">📐 L2 Vector Normalization</h4>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* XY Sliders */}
        <div className="bg-dark-card/40 border border-dark-border rounded p-3 space-y-3">
          <h5 className="font-bold text-slate-400 text-[10px] uppercase">Original Components</h5>

          <div className="space-y-1.5">
            <label className="flex justify-between">
              <span>Dimension X:</span>
              <span className="text-[#12DFFF] font-bold">{x.toFixed(1)}</span>
            </label>
            <input 
              type="range" min="-5" max="5" step="0.5" value={x}
              onChange={e => setX(parseFloat(e.target.value))}
              className="w-full accent-[#12DFFF]"
            />
          </div>

          <div className="space-y-1.5">
            <label className="flex justify-between">
              <span>Dimension Y:</span>
              <span className="text-[#12DFFF] font-bold">{y.toFixed(1)}</span>
            </label>
            <input 
              type="range" min="-5" max="5" step="0.5" value={y}
              onChange={e => setY(parseFloat(e.target.value))}
              className="w-full accent-[#12DFFF]"
            />
          </div>

          <button
            onClick={handleUpdate}
            disabled={running}
            className="w-full bg-brand/10 hover:bg-brand text-brand hover:text-dark-deep border border-brand/30 font-bold py-1.5 rounded transition-all flex justify-center items-center gap-1"
          >
            {running && <Loader2 className="w-3.5 h-3.5 animate-spin" />} Update Vector
          </button>
        </div>

        {/* Vector SVG Grid */}
        <div className="flex flex-col items-center bg-dark-card/40 border border-dark-border rounded p-3">
          <svg width={width} height={height} className="overflow-visible select-none">
            {/* Axes */}
            <line x1={0} y1={center} x2={width} y2={center} stroke="#1e293b" strokeWidth={1} />
            <line x1={center} y1={0} x2={center} y2={height} stroke="#1e293b" strokeWidth={1} />

            {/* Grid markings */}
            {[-5, -4, -3, -2, -1, 1, 2, 3, 4, 5].map((tick) => (
              <React.Fragment key={tick}>
                <line x1={mapX(tick)} y1={center - 3} x2={mapX(tick)} y2={center + 3} stroke="#334155" strokeWidth={1} />
                <line x1={center - 3} y1={mapY(tick)} x2={center + 3} y2={mapY(tick)} stroke="#334155" strokeWidth={1} />
              </React.Fragment>
            ))}

            {/* Arrow definitions */}
            <defs>
              <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#12DFFF" />
              </marker>
              <marker id="arrow-brand" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#c084fc" />
              </marker>
            </defs>

            {/* Original Vector */}
            <line 
              x1={center} y1={center} x2={mapX(data.original_vector[0])} y2={mapY(data.original_vector[1])}
              stroke="#12DFFF" strokeWidth={2.5} markerEnd="url(#arrow-blue)"
            />

            {/* Normalized Vector */}
            <line 
              x1={center} y1={center} x2={mapX(data.normalized_vector[0])} y2={mapY(data.normalized_vector[1])}
              stroke="#c084fc" strokeWidth={3} markerEnd="url(#arrow-brand)"
            />
          </svg>

          <div className="w-full mt-3 space-y-1 text-[10px] text-slate-400">
            <div className="flex justify-between">
              <span>Original magnitude:</span>
              <span className="text-[#12DFFF] font-bold">{data.magnitude?.toFixed(3)}</span>
            </div>
            <div className="flex justify-between">
              <span>Normalized vector:</span>
              <span className="text-[#c084fc] font-bold">[{data.normalized_vector[0]?.toFixed(2)}, {data.normalized_vector[1]?.toFixed(2)}]</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 4. MATRIX VISUALIZER
// ==========================================
interface MatrixVisualizerProps {
  data: { matrix_a: number[][]; matrix_b: number[][]; matrix_c: number[][] };
}
const MatrixVisualizer: React.FC<MatrixVisualizerProps> = ({ data }) => {
  const [hoveredCell, setHoveredCell] = useState<{ r: number; c: number } | null>(null);

  return (
    <div className="bg-dark-deep/40 border border-dark-border rounded-lg p-4 space-y-4 font-mono text-xs">
      <h4 className="text-xs font-bold text-slate-300">🧮 Matrix Multiplication (A × B = C)</h4>
      
      <p className="text-[10px] text-slate-500 leading-normal mb-2">
        Hover over a cell in the result matrix <b>C</b> to see the multiplying dot product rows of <b>A</b> and columns of <b>B</b>.
      </p>

      <div className="flex flex-col lg:flex-row items-center justify-center gap-6 overflow-x-auto py-2">
        {/* Matrix A */}
        <div>
          <h5 className="text-[9px] uppercase text-slate-500 mb-1.5 text-center">Matrix A</h5>
          <div className="border border-dark-border rounded p-1 bg-dark-card/20 inline-block">
            <table className="border-collapse">
              <tbody>
                {data.matrix_a.map((row, rIdx) => (
                  <tr key={rIdx}>
                    {row.map((val, cIdx) => (
                      <td 
                        key={cIdx} 
                        className={`w-12 h-10 text-center border border-dark-border/40 transition-colors ${
                          hoveredCell && hoveredCell.r === rIdx ? "bg-[#12DFFF]/20 text-[#12DFFF] font-bold" : "text-slate-300"
                        }`}
                      >
                        {val}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <span className="text-slate-600 font-bold text-base select-none">×</span>

        {/* Matrix B */}
        <div>
          <h5 className="text-[9px] uppercase text-slate-500 mb-1.5 text-center">Matrix B</h5>
          <div className="border border-dark-border rounded p-1 bg-dark-card/20 inline-block">
            <table className="border-collapse">
              <tbody>
                {data.matrix_b.map((row, rIdx) => (
                  <tr key={rIdx}>
                    {row.map((val, cIdx) => (
                      <td 
                        key={cIdx} 
                        className={`w-12 h-10 text-center border border-dark-border/40 transition-colors ${
                          hoveredCell && hoveredCell.c === cIdx ? "bg-purple-500/20 text-purple-300 font-bold" : "text-slate-300"
                        }`}
                      >
                        {val}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <span className="text-slate-600 font-bold text-base select-none">=</span>

        {/* Matrix C */}
        <div>
          <h5 className="text-[9px] uppercase text-slate-500 mb-1.5 text-center">Result C</h5>
          <div className="border border-brand/30 rounded p-1 bg-dark-card/40 inline-block">
            <table className="border-collapse">
              <tbody>
                {data.matrix_c.map((row, rIdx) => (
                  <tr key={rIdx}>
                    {row.map((val, cIdx) => (
                      <td 
                        key={cIdx} 
                        onMouseEnter={() => setHoveredCell({ r: rIdx, c: cIdx })}
                        onMouseLeave={() => setHoveredCell(null)}
                        className={`w-12 h-10 text-center border border-dark-border/40 transition-colors cursor-crosshair font-bold ${
                          hoveredCell && hoveredCell.r === rIdx && hoveredCell.c === cIdx
                            ? "bg-brand text-dark-deep"
                            : "text-brand hover:bg-dark-border/50"
                        }`}
                      >
                        {val}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {hoveredCell && (
        <div className="p-3 bg-dark-card/60 border border-dark-border rounded text-[11px] text-slate-400">
          <span className="text-white font-bold text-brand uppercase text-[9px] block mb-1">Dot Product formula:</span>
          C[{hoveredCell.r}, {hoveredCell.c}] = {" "}
          {data.matrix_a[hoveredCell.r].map((a_val, idx) => (
            <span key={idx}>
              {idx > 0 && " + "}
              ({a_val} x {data.matrix_b[idx][hoveredCell.c]})
            </span>
          ))}
          {" = "}
          <span className="text-brand font-bold">{data.matrix_c[hoveredCell.r][hoveredCell.c]}</span>
        </div>
      )}
    </div>
  );
};

// ==========================================
// 5. GRADIENT DESCENT VISUALIZER
// ==========================================
interface GradientDescentVisualizerProps {
  data: {
    steps: { epoch: number; loss: number; weight: number; derivative: number; w_new?: number }[];
    learning_rate: number;
    target_weight: number;
  };
  currentStep: number;
  setCurrentStep: React.Dispatch<React.SetStateAction<number>>;
  isPlaying: boolean;
  setIsPlaying: React.Dispatch<React.SetStateAction<boolean>>;
  playbackSpeed: number;
  setPlaybackSpeed: React.Dispatch<React.SetStateAction<number>>;
  onUpdate: (inputs: any) => void;
  running: boolean;
}
const GradientDescentVisualizer: React.FC<GradientDescentVisualizerProps> = ({
  data,
  currentStep,
  setCurrentStep,
  isPlaying,
  setIsPlaying,
  playbackSpeed,
  setPlaybackSpeed,
  onUpdate,
  running
}) => {
  const [lr, setLr] = useState(data.learning_rate || 0.1);
  const [iters, setIters] = useState(data.steps?.length || 20);

  const steps = data.steps || [];
  const activeStep = steps[currentStep] || steps[0] || { epoch: 0, loss: 0.0, weight: 0.0, derivative: 0.0 };
  const w = activeStep.weight;
  const dw = activeStep.derivative;
  const learningRate = data.learning_rate ?? lr;
  const w_new = activeStep.w_new !== undefined ? activeStep.w_new : (w - learningRate * dw);

  const handleApply = () => {
    onUpdate({ learning_rate: lr, iterations: iters });
  };

  const chartWidth = 320;
  const chartHeight = 110;
  const padding = 15;

  // Max bounds
  const maxLoss = Math.max(...steps.map(s => s.loss), 1.0);
  const minWeight = Math.min(...steps.map(s => s.weight), 0.0);
  const maxWeight = Math.max(...steps.map(s => s.weight), 2.5);

  const mapEpoch = (epoch: number) => steps.length > 1 ? padding + (epoch / (steps.length - 1)) * (chartWidth - 2 * padding) : chartWidth / 2;
  const mapLoss = (loss: number) => chartHeight - padding - (loss / maxLoss) * (chartHeight - 2 * padding);
  const mapWeight = (wVal: number) => {
    const range = (maxWeight - minWeight) || 1.0;
    return chartHeight - padding - ((wVal - minWeight) / range) * (chartHeight - 2 * padding);
  };

  const lossPoints = steps
    .map(s => `${mapEpoch(s.epoch)},${mapLoss(s.loss)}`)
    .join(" ");

  const weightPoints = steps
    .map(s => `${mapEpoch(s.epoch)},${mapWeight(s.weight)}`)
    .join(" ");

  // Visual parameter movement bounds (SVG)
  const axisWidth = 320;
  const axisHeight = 50;
  const axisMin = Math.min(w, w_new, -0.5);
  const axisMax = Math.max(w, w_new, 2.5);
  const axisRange = (axisMax - axisMin) || 1.0;
  const mapAxisX = (val: number) => 20 + ((val - axisMin) / axisRange) * (axisWidth - 40);

  return (
    <div className="bg-dark-deep/40 border border-dark-border rounded-lg p-4 space-y-4 font-mono text-xs">
      <h4 className="text-xs font-bold text-slate-300">📉 Iterative Gradient Descent Convergence</h4>

      {/* Speed & Steps Playback controls */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-3 bg-dark-card border border-dark-border rounded-md">
        
        <div className="flex items-center gap-1.5">
          <button
            onClick={() => {
              setIsPlaying(false);
              setCurrentStep(0);
            }}
            className="p-1 hover:bg-dark-border text-slate-400 hover:text-white rounded"
            title="Reset"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
          
          <button
            onClick={() => {
              setIsPlaying(false);
              setCurrentStep(prev => Math.max(0, prev - 1));
            }}
            className="p-1 hover:bg-dark-border text-slate-400 hover:text-white rounded"
            title="Step Back"
          >
            <SkipBack className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="px-2.5 py-1 bg-brand text-dark-deep hover:bg-brand-dark rounded font-bold text-[10px] uppercase flex items-center gap-1 transition-all"
          >
            {isPlaying ? <Pause className="w-3 h-3 fill-dark-deep" /> : <Play className="w-3 h-3 fill-dark-deep" />}
            {isPlaying ? "Pause" : "Play"}
          </button>

          <button
            onClick={() => {
              setIsPlaying(false);
              setCurrentStep(prev => Math.min(steps.length - 1, prev + 1));
            }}
            className="p-1 hover:bg-dark-border text-slate-400 hover:text-white rounded"
            title="Step Forward"
          >
            <SkipForward className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Active iteration */}
        <div className="text-[10px] text-slate-400">
          Iteration: <span className="text-brand font-bold">{currentStep + 1}</span> / {steps.length}
        </div>

        {/* Speed selectors */}
        <div className="flex border border-dark-border rounded overflow-hidden text-[9px] bg-dark-deep">
          {[0.5, 1, 2].map((s) => (
            <button
              key={s}
              onClick={() => setPlaybackSpeed(s)}
              className={`px-2 py-0.5 border-r border-dark-border last:border-0 ${
                playbackSpeed === s ? "bg-brand text-dark-deep font-bold" : "text-slate-400 hover:text-white"
              }`}
            >
              {s}x
            </button>
          ))}
        </div>
      </div>

      {/* Mathematical Update Formula Box */}
      <div className="bg-dark-card/60 border border-[#12DFFF]/30 rounded-md p-3 space-y-2">
        <div className="flex justify-between items-center text-[10px] uppercase font-bold text-[#12DFFF]">
          <span>Mathematical Update Relationship</span>
          <span>w_new = w - (learning_rate × dw)</span>
        </div>
        <div className="bg-dark-deep p-2 rounded border border-dark-border/60 text-xs font-mono flex flex-wrap items-center justify-between gap-2 text-slate-200">
          <div>
            <span className="text-[#c084fc] font-bold">{w_new.toFixed(4)}</span>
            <span className="text-slate-500"> = </span>
            <span className="text-[#12DFFF] font-bold">{w.toFixed(4)}</span>
            <span className="text-slate-500"> - (</span>
            <span className="text-amber-400 font-bold">{learningRate.toFixed(4)}</span>
            <span className="text-slate-500"> × </span>
            <span className="text-emerald-400 font-bold">{dw.toFixed(4)}</span>
            <span className="text-slate-500">)</span>
          </div>
          <div className="text-[10px] text-slate-400">
            Δw = <span className="text-brand font-bold">{(w_new - w).toFixed(4)}</span>
          </div>
        </div>
      </div>

      {/* Visual Parameter Movement / Update Axis */}
      <div className="bg-dark-card/40 border border-dark-border rounded p-3 flex flex-col items-center">
        <h5 className="text-[9px] uppercase text-slate-400 mb-1 font-bold">Visual Parameter Movement Track (w → w_new)</h5>
        <svg width={axisWidth} height={axisHeight} className="overflow-visible select-none">
          <line x1={20} y1={25} x2={axisWidth - 20} y2={25} stroke="#334155" strokeWidth={2} />
          
          {/* Movement Vector line */}
          <line 
            x1={mapAxisX(w)} y1={25} 
            x2={mapAxisX(w_new)} y2={25} 
            stroke="#12DFFF" strokeWidth={4} strokeDasharray="4 2"
          />

          {/* Current Parameter Marker w */}
          <circle cx={mapAxisX(w)} cy={25} r={6} fill="#12DFFF" />
          <text x={mapAxisX(w)} y={12} textAnchor="middle" fill="#12DFFF" fontSize={9} fontWeight="bold">
            w: {w.toFixed(2)}
          </text>

          {/* Updated Parameter Marker w_new */}
          <circle cx={mapAxisX(w_new)} cy={25} r={6} fill="#c084fc" />
          <text x={mapAxisX(w_new)} y={42} textAnchor="middle" fill="#c084fc" fontSize={9} fontWeight="bold">
            w_new: {w_new.toFixed(2)}
          </text>
        </svg>
      </div>

      {/* Parameter update sliders & State Telemetry */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-dark-card/30 border border-dark-border rounded p-3 space-y-3">
          <h5 className="font-bold text-slate-400 text-[10px] uppercase">Hyperparameters</h5>

          <div className="space-y-1">
            <label className="flex justify-between text-[11px]">
              <span>Learning Rate:</span>
              <span className="text-[#12DFFF] font-bold">{lr.toFixed(2)}</span>
            </label>
            <input
              type="range" min="0.01" max="0.5" step="0.01" value={lr}
              onChange={e => setLr(parseFloat(e.target.value))}
              className="w-full accent-[#12DFFF]"
            />
          </div>

          <div className="space-y-1">
            <label className="flex justify-between text-[11px]">
              <span>Iterations:</span>
              <span className="text-[#12DFFF] font-bold">{iters}</span>
            </label>
            <input
              type="range" min="5" max="50" step="5" value={iters}
              onChange={e => setIters(parseInt(e.target.value))}
              className="w-full accent-[#12DFFF]"
            />
          </div>

          <button
            onClick={handleApply}
            disabled={running}
            className="w-full bg-[#12DFFF]/10 hover:bg-[#12DFFF] text-[#12DFFF] hover:text-dark-deep border border-[#12DFFF]/30 py-1.5 font-bold rounded transition-all text-xs flex justify-center items-center gap-1"
          >
            {running && <Loader2 className="w-3.5 h-3.5 animate-spin" />} Run Trajectory
          </button>
        </div>

        {/* Current Iteration metrics */}
        <div className="bg-dark-card/30 border border-dark-border rounded p-3 flex flex-col justify-between">
          <h5 className="font-bold text-slate-400 text-[10px] uppercase">State Telemetry</h5>
          <div className="grid grid-cols-2 gap-2 text-xs py-2">
            <div className="bg-dark-deep/40 p-2 rounded border border-dark-border/40">
              <span className="text-[10px] text-slate-500">Current Parameter (w)</span>
              <div className="text-[#12DFFF] font-bold text-sm mt-0.5">{w.toFixed(4)}</div>
            </div>
            <div className="bg-dark-deep/40 p-2 rounded border border-dark-border/40">
              <span className="text-[10px] text-slate-500">Gradient (dw)</span>
              <div className="text-emerald-400 font-bold text-sm mt-0.5">{dw.toFixed(4)}</div>
            </div>
            <div className="bg-dark-deep/40 p-2 rounded border border-dark-border/40">
              <span className="text-[10px] text-slate-500">Learning Rate (η)</span>
              <div className="text-amber-400 font-bold text-sm mt-0.5">{learningRate.toFixed(4)}</div>
            </div>
            <div className="bg-dark-deep/40 p-2 rounded border border-dark-border/40">
              <span className="text-[10px] text-slate-500">Updated Parameter (w_new)</span>
              <div className="text-[#c084fc] font-bold text-sm mt-0.5">{w_new.toFixed(4)}</div>
            </div>
          </div>
          <p className="text-[9px] text-slate-500">Target minimum: w = {data.target_weight}</p>
        </div>
      </div>

      {/* Convergence Graphs */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Loss chart */}
        <div className="bg-dark-card/40 border border-dark-border rounded p-3 flex flex-col items-center">
          <h5 className="text-[9px] uppercase text-slate-400 mb-2 font-bold">Loss Convergence Curve</h5>
          <svg width={chartWidth} height={chartHeight} className="overflow-visible">
            <polyline fill="none" stroke="#ef4444" strokeWidth={1.5} points={lossPoints} />
            <circle cx={mapEpoch(activeStep.epoch)} cy={mapLoss(activeStep.loss)} r={4} fill="#ef4444" />
          </svg>
        </div>

        {/* Weights chart */}
        <div className="bg-dark-card/40 border border-dark-border rounded p-3 flex flex-col items-center">
          <h5 className="text-[9px] uppercase text-slate-400 mb-2 font-bold">Weight Value (w) vs Epoch</h5>
          <svg width={chartWidth} height={chartHeight} className="overflow-visible">
            <polyline fill="none" stroke="#a855f7" strokeWidth={1.5} points={weightPoints} />
            <circle cx={mapEpoch(activeStep.epoch)} cy={mapWeight(activeStep.weight)} r={4} fill="#a855f7" />
          </svg>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 6. LINEAR REGRESSION VISUALIZER
// ==========================================
interface LinearRegressionVisualizerProps {
  data: { X: number[][]; weights: number[]; bias: number; predictions: number[] };
  onUpdate: (inputs: any) => void;
  running: boolean;
}
const LinearRegressionVisualizer: React.FC<LinearRegressionVisualizerProps> = ({ data, onUpdate, running }) => {
  const [w, setW] = useState(data.weights[0] || 2.0);
  const [b, setB] = useState(data.bias || 1.0);

  const handleUpdate = () => {
    onUpdate({ weights: [w], bias: b });
  };

  const chartSize = 180;
  const padding = 20;

  // Map 1D x: [0, 5], y: [0, 12]
  const mapX = (val: number) => padding + (val / 5) * (chartSize - 2 * padding);
  const mapY = (val: number) => chartSize - padding - (val / 12) * (chartSize - 2 * padding);

  // Line points
  const xStart = 0;
  const yStart = w * xStart + b;
  const xEnd = 5;
  const yEnd = w * xEnd + b;

  return (
    <div className="bg-dark-deep/40 border border-dark-border rounded-lg p-4 space-y-4 font-mono text-xs">
      <h4 className="text-xs font-bold text-slate-300">📈 Linear Regression Predictor</h4>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Sliders */}
        <div className="bg-dark-card/40 border border-dark-border rounded p-3 space-y-3">
          <h5 className="font-bold text-slate-400 text-[10px] uppercase">Parameters</h5>

          <div className="space-y-1.5">
            <label className="flex justify-between">
              <span>Weight (Slope):</span>
              <span className="text-[#12DFFF] font-bold">{w.toFixed(1)}</span>
            </label>
            <input 
              type="range" min="0" max="4" step="0.2" value={w}
              onChange={e => setW(parseFloat(e.target.value))}
              className="w-full accent-[#12DFFF]"
            />
          </div>

          <div className="space-y-1.5">
            <label className="flex justify-between">
              <span>Bias (Intercept):</span>
              <span className="text-[#12DFFF] font-bold">{b.toFixed(1)}</span>
            </label>
            <input 
              type="range" min="-2" max="5" step="0.5" value={b}
              onChange={e => setB(parseFloat(e.target.value))}
              className="w-full accent-[#12DFFF]"
            />
          </div>

          <button
            onClick={handleUpdate}
            disabled={running}
            className="w-full bg-[#12DFFF]/10 hover:bg-[#12DFFF] text-[#12DFFF] hover:text-dark-deep border border-[#12DFFF]/30 font-bold py-1.5 rounded transition-all text-xs flex justify-center items-center gap-1"
          >
            {running && <Loader2 className="w-3.5 h-3.5 animate-spin" />} Update Regression Line
          </button>
        </div>

        {/* SVG Plot */}
        <div className="flex flex-col items-center bg-dark-card/40 border border-dark-border rounded p-3">
          <svg width={chartSize} height={chartSize} className="overflow-visible select-none">
            {/* Axis markings */}
            <line x1={padding} y1={chartSize - padding} x2={chartSize - padding} y2={chartSize - padding} stroke="#1e293b" />
            <line x1={padding} y1={padding} x2={padding} y2={chartSize - padding} stroke="#1e293b" />

            {/* Regression Line */}
            <line 
              x1={mapX(xStart)} y1={mapY(yStart)} 
              x2={mapX(xEnd)} y2={mapY(yEnd)} 
              stroke="#12DFFF" strokeWidth={2} 
            />

            {/* Data points */}
            {data.X.map((xArr, idx) => (
              <circle 
                key={idx} 
                cx={mapX(xArr[0])} 
                cy={mapY(data.predictions[idx])} 
                r={4.5} 
                fill="#FF4FA3" 
              />
            ))}
          </svg>

          <div className="w-full mt-3 text-[10px] text-slate-500">
            Current equation: <span className="text-[#12DFFF] font-bold">y = {w.toFixed(1)}x + {b.toFixed(1)}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 7. K-MEANS VISUALIZER
// ==========================================
interface KMeansVisualizerProps {
  data: { X: number[][]; centroids: number[][]; assignments: number[] };
}
const KMeansVisualizer: React.FC<KMeansVisualizerProps> = ({ data }) => {
  const width = 240;
  const height = 160;
  const padding = 15;

  // Map coordinates in [0, 8] range
  const mapX = (v: number) => padding + (v / 8) * (width - 2 * padding);
  const mapY = (v: number) => height - padding - (v / 8) * (height - 2 * padding);

  const colors = ["#12DFFF", "#a855f7", "#22c55e", "#eab308"];

  return (
    <div className="bg-dark-deep/40 border border-dark-border rounded-lg p-4 space-y-4 font-mono text-xs">
      <h4 className="text-xs font-bold text-slate-300">📌 K-Means Centroid Assignments</h4>

      <div className="flex flex-col items-center bg-dark-card/40 border border-dark-border rounded p-3">
        <svg width={width} height={height} className="overflow-visible select-none">
          <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} stroke="#1e293b" />
          <line x1={padding} y1={padding} x2={padding} y2={height - padding} stroke="#1e293b" />

          {/* Draw cluster elements */}
          {data.X.map((pt, idx) => {
            const cluster = data.assignments[idx];
            return (
              <circle
                key={idx}
                cx={mapX(pt[0])}
                cy={mapY(pt[1])}
                r={4}
                fill={colors[cluster] || "#94a3b8"}
              />
            );
          })}

          {/* Draw centroids */}
          {data.centroids.map((c, idx) => (
            <polygon
              key={idx}
              points={`${mapX(c[0])},${mapY(c[1]) - 6} ${mapX(c[0]) - 5},${mapY(c[1]) + 4} ${mapX(c[0]) + 5},${mapY(c[1]) + 4}`}
              fill="#ef4444"
              stroke="white"
              strokeWidth={1}
            />
          ))}
        </svg>

        <div className="w-full mt-3 flex justify-between text-[10px] text-slate-400">
          <span>Points Count: {data.X.length}</span>
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 bg-red-500 rotate-45 border border-white" /> Centroids
          </span>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 8. PCA VISUALIZER
// ==========================================
interface PcaVisualizerProps {
  data: { X: number[][]; components: number[][]; projection: number[] };
}
const PcaVisualizer: React.FC<PcaVisualizerProps> = ({ data }) => {
  const size = 180;
  const padding = 15;
  const mapX = (v: number) => padding + ((v + 2) / 6) * (size - 2 * padding);
  const mapY = (v: number) => size - padding - ((v + 2) / 6) * (size - 2 * padding);

  return (
    <div className="bg-dark-deep/40 border border-dark-border rounded-lg p-4 space-y-4 font-mono text-xs">
      <h4 className="text-xs font-bold text-slate-300">🧬 PCA Linear Component Projection</h4>

      <div className="flex flex-col items-center bg-dark-card/40 border border-dark-border rounded p-3">
        <svg width={size} height={size} className="overflow-visible select-none">
          <line x1={0} y1={size/2} x2={size} y2={size/2} stroke="#1e293b" />
          <line x1={size/2} y1={0} x2={size/2} y2={size} stroke="#1e293b" />

          {/* Original points */}
          {data.X.map((pt, idx) => (
            <circle key={idx} cx={mapX(pt[0])} cy={mapY(pt[1])} r={4.5} fill="#3b82f6" />
          ))}

          {/* Principal Axis direction */}
          {data.components && data.components[0] && (
            <line 
              x1={mapX(-data.components[0][0] * 3)} y1={mapY(-data.components[1][0] * 3)}
              x2={mapX(data.components[0][0] * 3)} y2={mapY(data.components[1][0] * 3)}
              stroke="#12DFFF" strokeDasharray="3,3" strokeWidth={1.5}
            />
          )}
        </svg>

        <div className="w-full mt-3 text-[10px] text-slate-500">
          Projected 1D coords: <span className="text-[#12DFFF] font-bold">[{data.projection.map(v => v.toFixed(2)).join(", ")}]</span>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 9. DENSE LAYER VISUALIZER
// ==========================================
interface DenseLayerVisualizerProps {
  data: { X: number[][]; weights: number[][]; bias: number[]; output: number[] };
}
const DenseLayerVisualizer: React.FC<DenseLayerVisualizerProps> = ({ data }) => {
  return (
    <div className="bg-dark-deep/40 border border-dark-border rounded-lg p-4 space-y-4 font-mono text-xs">
      <h4 className="text-xs font-bold text-slate-300">🧠 Neural Network Layer Connections</h4>

      <div className="flex flex-col items-center bg-dark-card/40 border border-dark-border rounded p-4">
        <svg width="300" height="150" className="overflow-visible select-none">
          {/* Layer 1 Nodes (Inputs) */}
          <circle cx="50" cy="40" r="14" fill="#1e293b" stroke="#12DFFF" strokeWidth={1.5} />
          <text x="50" y="43" fill="white" fontSize="9" textAnchor="middle">{data.X[0][0]?.toFixed(1)}</text>
          
          <circle cx="50" cy="110" r="14" fill="#1e293b" stroke="#12DFFF" strokeWidth={1.5} />
          <text x="50" y="113" fill="white" fontSize="9" textAnchor="middle">{data.X[0][1]?.toFixed(1)}</text>

          {/* Connections / Lines */}
          <line x1="64" y1="40" x2="236" y2="40" stroke="#475569" strokeWidth={1.5} />
          <line x1="64" y1="40" x2="236" y2="110" stroke="#475569" strokeWidth={1} />
          <line x1="64" y1="110" x2="236" y2="40" stroke="#475569" strokeWidth={1} />
          <line x1="64" y1="110" x2="236" y2="110" stroke="#475569" strokeWidth={1.5} />

          {/* Layer 2 Nodes (Outputs) */}
          <circle cx="250" cy="40" r="14" fill="#1e293b" stroke="#a855f7" strokeWidth={1.5} />
          <text x="250" y="43" fill="white" fontSize="9" textAnchor="middle">{data.output[0]?.toFixed(1)}</text>
          
          <circle cx="250" cy="110" r="14" fill="#1e293b" stroke="#a855f7" strokeWidth={1.5} />
          <text x="250" y="113" fill="white" fontSize="9" textAnchor="middle">{data.output[1]?.toFixed(1)}</text>

          {/* Descriptions */}
          <text x="50" y="15" fill="#8B958E" fontSize="8" textAnchor="middle">INPUT</text>
          <text x="250" y="15" fill="#8B958E" fontSize="8" textAnchor="middle">OUTPUT</text>
        </svg>
      </div>
    </div>
  );
};

// ==========================================
// 10. NEURAL NETWORK VISUALIZER
// ==========================================
interface NeuralNetworkVisualizerProps {
  data: { X: number[][]; W1: number[][]; b1: number[]; W2: number[][]; b2: number[]; output: number[] };
}
const NeuralNetworkVisualizer: React.FC<NeuralNetworkVisualizerProps> = ({ data }) => {
  return (
    <div className="bg-dark-deep/40 border border-dark-border rounded-lg p-4 space-y-4 font-mono text-xs">
      <h4 className="text-xs font-bold text-slate-300">🧠 2-Layer Neural Network Feedforward</h4>

      <div className="flex flex-col items-center bg-dark-card/40 border border-dark-border rounded p-4">
        <svg width="340" height="150" className="overflow-visible select-none">
          {/* Layer 1 Nodes (Inputs) */}
          <circle cx="40" cy="40" r="12" fill="#1e293b" stroke="#12DFFF" strokeWidth={1.5} />
          <text x="40" y="43" fill="white" fontSize="8" textAnchor="middle">{data.X[0][0]?.toFixed(1)}</text>
          
          <circle cx="40" cy="110" r="12" fill="#1e293b" stroke="#12DFFF" strokeWidth={1.5} />
          <text x="40" y="113" fill="white" fontSize="8" textAnchor="middle">{data.X[0][1]?.toFixed(1)}</text>

          {/* Hidden layer */}
          <circle cx="170" cy="40" r="12" fill="#1e293b" stroke="#a855f7" strokeWidth={1.5} />
          <circle cx="170" cy="110" r="12" fill="#1e293b" stroke="#a855f7" strokeWidth={1.5} />

          {/* Output node */}
          <circle cx="300" cy="75" r="12" fill="#1e293b" stroke="#eab308" strokeWidth={1.5} />
          <text x="300" y="78" fill="white" fontSize="8" textAnchor="middle">{data.output[0]?.toFixed(2)}</text>

          {/* Connections L1 -> L2 */}
          <line x1="52" y1="40" x2="158" y2="40" stroke="#334155" />
          <line x1="52" y1="40" x2="158" y2="110" stroke="#334155" />
          <line x1="52" y1="110" x2="158" y2="40" stroke="#334155" />
          <line x1="52" y1="110" x2="158" y2="110" stroke="#334155" />

          {/* Connections L2 -> L3 */}
          <line x1="182" y1="40" x2="288" y2="75" stroke="#334155" />
          <line x1="182" y1="110" x2="288" y2="75" stroke="#334155" />

          <text x="40" y="15" fill="#8B958E" fontSize="8" textAnchor="middle">INPUT</text>
          <text x="170" y="15" fill="#8B958E" fontSize="8" textAnchor="middle">HIDDEN</text>
          <text x="300" y="15" fill="#8B958E" fontSize="8" textAnchor="middle">OUTPUT</text>
        </svg>
      </div>
    </div>
  );
};

// ==========================================
// 11. SCALED DOT PRODUCT VISUALIZER
// ==========================================
interface ScaledDotProductVisualizerProps {
  data: { Q: number[][]; K: number[][]; V: number[][]; output: number[][] };
}
const ScaledDotProductVisualizer: React.FC<ScaledDotProductVisualizerProps> = ({ data }) => {
  return (
    <div className="bg-dark-deep/40 border border-dark-border rounded-lg p-4 space-y-4 font-mono text-xs">
      <h4 className="text-xs font-bold text-slate-300">⚡ Scaled Dot-Product Attention Flow</h4>
      <div className="bg-dark-card/40 border border-dark-border rounded p-3 space-y-2">
        <div className="flex justify-between">
          <span className="text-slate-500">Query (Q):</span>
          <span className="text-[#12DFFF] font-bold">[{data.Q.map(r => `[${r.join(",")}]`).join(",")}]</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">Key (K):</span>
          <span className="text-[#12DFFF] font-bold">[{data.K.map(r => `[${r.join(",")}]`).join(",")}]</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">Value (V):</span>
          <span className="text-[#c084fc] font-bold">[{data.V.map(r => `[${r.join(",")}]`).join(",")}]</span>
        </div>
        <div className="flex justify-between border-t border-dark-border pt-1.5 mt-1.5">
          <span className="text-slate-300 font-bold">Attention Output:</span>
          <span className="text-brand font-bold">[{data.output.map(r => `[${r.map(v => v.toFixed(2)).join(",")}]`).join(",")}]</span>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 12. ATTENTION SCORES VISUALIZER (Heatmap)
// ==========================================
interface AttentionScoresVisualizerProps {
  data: { Q: number[][]; K: number[][]; attention_matrix: number[][] };
}
const AttentionScoresVisualizer: React.FC<AttentionScoresVisualizerProps> = ({ data }) => {
  const [hoveredScore, setHoveredScore] = useState<{ r: number; c: number; score: number } | null>(null);

  return (
    <div className="bg-dark-deep/40 border border-dark-border rounded-lg p-4 space-y-4 font-mono text-xs">
      <h4 className="text-xs font-bold text-slate-300">🔥 Scaled Dot Product Attention Scores Matrix</h4>

      <div className="flex flex-col items-center bg-dark-card/40 border border-dark-border rounded p-4">
        <div className="grid grid-cols-2 gap-2 relative">
          {data.attention_matrix.map((row, rIdx) => 
            row.map((score, cIdx) => (
              <div 
                key={`${rIdx}-${cIdx}`}
                onMouseEnter={() => setHoveredScore({ r: rIdx, c: cIdx, score: score })}
                onMouseLeave={() => setHoveredScore(null)}
                className="w-16 h-16 border border-dark-border flex items-center justify-center font-bold cursor-crosshair transition-colors"
                style={{ 
                  backgroundColor: `rgba(0, 242, 254, ${score})`,
                  color: score > 0.5 ? "#020617" : "#12DFFF"
                }}
              >
                {score.toFixed(3)}
              </div>
            ))
          )}
        </div>

        {hoveredScore && (
          <div className="mt-3 p-2 bg-dark-deep border border-dark-border rounded text-[10px] text-slate-400">
            Query token <span className="text-brand font-bold">#{hoveredScore.r + 1}</span> attends to Key token <span className="text-brand font-bold">#{hoveredScore.c + 1}</span> with score: <span className="text-[#12DFFF] font-bold">{hoveredScore.score.toFixed(4)}</span>
          </div>
        )}
      </div>
    </div>
  );
};

// ==========================================
// 13. SELF ATTENTION VISUALIZER
// ==========================================
interface SelfAttentionVisualizerProps {
  data: { X: number[][]; W_q: number[][]; W_k: number[][]; W_v: number[][]; output: number[][] };
}
const SelfAttentionVisualizer: React.FC<SelfAttentionVisualizerProps> = ({ data }) => {
  return (
    <div className="bg-dark-deep/40 border border-dark-border rounded-lg p-4 space-y-4 font-mono text-xs">
      <h4 className="text-xs font-bold text-slate-300">⚡ Transformer Self-Attention outputs</h4>
      <div className="p-3 bg-dark-card/40 border border-dark-border rounded space-y-2">
        <div className="flex justify-between">
          <span className="text-slate-500">Inputs (X):</span>
          <span className="text-slate-300">[{data.X.map(r => `[${r.join(",")}]`).join(",")}]</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">Query projection weights:</span>
          <span className="text-[#12DFFF]">[{data.W_q.map(r => `[${r.join(",")}]`).join(",")}]</span>
        </div>
        <div className="flex justify-between border-t border-dark-border pt-1.5 mt-1.5">
          <span className="text-slate-300 font-bold">Attended values output:</span>
          <span className="text-brand font-bold">[{data.output.map(r => `[${r.map(v => v.toFixed(2)).join(",")}]`).join(",")}]</span>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 14. EMBEDDING SIMILARITY VISUALIZER
// ==========================================
interface EmbeddingSimilarityVisualizerProps {
  data: { query: number[]; document: number[]; similarity: number };
}
const EmbeddingSimilarityVisualizer: React.FC<EmbeddingSimilarityVisualizerProps> = ({ data }) => {
  return (
    <div className="bg-dark-deep/40 border border-dark-border rounded-lg p-4 space-y-4 font-mono text-xs">
      <h4 className="text-xs font-bold text-slate-300">🔗 Vector Embedding Similarity metric</h4>
      <div className="p-3 bg-dark-card/40 border border-dark-border rounded space-y-2">
        <div className="flex justify-between">
          <span className="text-slate-500">Query Vector:</span>
          <span className="text-[#12DFFF] font-bold">[{data.query.join(", ")}]</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">Document Vector:</span>
          <span className="text-[#c084fc] font-bold">[{data.document.join(", ")}]</span>
        </div>
        <div className="flex justify-between border-t border-dark-border pt-1.5 mt-1.5">
          <span className="text-slate-300 font-bold">Cosine Similarity:</span>
          <span className="text-brand font-bold">{data.similarity?.toFixed(4)}</span>
        </div>
      </div>
    </div>
  );
};
