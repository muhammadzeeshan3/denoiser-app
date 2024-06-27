import torch
import os
import torchaudio
import matplotlib.pyplot as plt
import numpy as np
from django.conf import settings
from uuid import uuid4
from resemble_enhance.enhancer.inference import denoise, enhance

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"


def plot_waveform(waveform, sample_rate, title, file_name):
    plt.figure(figsize=(10, 4))
    time_axis = np.arange(0, len(waveform)) / sample_rate
    plt.plot(time_axis, waveform)
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()


def _fn(input_path, solver, nfe, tau, denoising, output_denoised_path, output_enhanced_path):
    if input_path is None:
        return None, None

    graphs_dir = os.path.join(settings.MEDIA_ROOT, 'graphs')
    os.makedirs(graphs_dir, exist_ok=True)

    solver = solver.lower()
    nfe = int(nfe)
    lambd = 0.9 if denoising else 0.1

    dwav, sr = torchaudio.load(input_path)
    dwav = dwav.mean(dim=0)

    wav1, new_sr = denoise(dwav, sr, device)
    wav2, new_sr = enhance(dwav, sr, device, nfe=nfe, solver=solver, lambd=lambd, tau=tau)

    wav1 = wav1.cpu().numpy()
    wav2 = wav2.cpu().numpy()

    torchaudio.save(output_denoised_path, torch.tensor(wav1).unsqueeze(0), new_sr)
    torchaudio.save(output_enhanced_path, torch.tensor(wav2).unsqueeze(0), new_sr)

    # Plot and save the waveforms
    plot_original_path = graphs_dir + f"/{uuid4().hex}.jpeg"
    plot_denoised_path = graphs_dir + f"/{uuid4().hex}.jpeg"

    plot_waveform(dwav.cpu().numpy(), sr, 'Original Waveform', plot_original_path)
    plot_waveform(wav1, new_sr, 'Denoised Waveform', plot_denoised_path)

    return output_denoised_path, plot_original_path, plot_denoised_path


def start_process(filename):
    file_path = settings.MEDIA_ROOT + f"/{filename}"
    solver = "Midpoint"
    nfe = 64
    tau = 0.5
    denoising = False

    outputs_dir = os.path.join(settings.MEDIA_ROOT, 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)

    output_denoised_path = outputs_dir + f'/{uuid4().hex}.wav'
    output_enhanced_path = outputs_dir + f'/{uuid4().hex}.wav'

    print("Reached here", file_path)

    denoised_audio_path, plot_original_path, plot_denoised_path = _fn(
        file_path,
        solver,
        nfe,
        tau,
        denoising,
        output_denoised_path,
        output_enhanced_path,
    )

    return denoised_audio_path, plot_original_path, plot_denoised_path
