#!/bin/bash
#SBATCH --job-name=vision-caption
#SBATCH --output=logs/vision_caption_%j.log
#SBATCH --error=logs/vision_caption_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --gres=gpu:1
#SBATCH --time=04:00:00
#SBATCH --partition=gpu

# ── Setup ambiente ────────────────────────────────────────────────────────────
echo "Starting vision-caption on $(hostname) at $(date)"
echo "Job ID: $SLURM_JOB_ID"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'N/A')"

# Carica moduli SLURM (adatta al cluster PurpleJeans)
# module load python/3.12
# module load cuda/12.1

cd "$SLURM_SUBMIT_DIR" || exit 1
export PATH="$HOME/.local/bin:$PATH"

mkdir -p logs

# ── Installa vision-commons (path dep) se necessario ─────────────────────────
if [ ! -d "../vision-commons/.venv" ]; then
    echo "Installing vision-commons..."
    pushd ../vision-commons && poetry install --without dev && popd
fi

# ── Avvia Ollama in background ────────────────────────────────────────────────
echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!
sleep 5

if ! ollama list | grep -q "gemma4"; then
    echo "Pulling gemma4:e4b model..."
    ollama pull gemma4:e4b
fi

# ── Avvia vision-caption server ───────────────────────────────────────────────
echo "Starting vision-caption server..."
poetry run python -m vision_caption \
    --host 0.0.0.0 \
    --port 8765 \
    --log-level INFO

# Cleanup
echo "Stopping Ollama..."
kill $OLLAMA_PID 2>/dev/null

echo "Job completed at $(date)"
