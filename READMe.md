# 🧠 NeuroLearn
### BCI-Powered Adaptive Learning for Neurodiverse Individuals

> *Transforming frustration into focus — one brainwave at a time.*

[![Domain](https://img.shields.io/badge/Domain-AI%20%2F%20ML-blueviolet)](https://github.com/)
[![Hardware](https://img.shields.io/badge/Hardware-EEG%20%2B%20Arduino-green)](https://github.com/)
[![Accuracy](https://img.shields.io/badge/Model%20Accuracy-96.4%25-brightgreen)](https://github.com/)
[![Institution](https://img.shields.io/badge/Institution-SIES%20GST%20Navi%20Mumbai-blue)](https://github.com/)

---

## 📖 Overview

**NeuroLearn** is an end-to-end, real-time adaptive learning platform that uses **Brain-Computer Interface (BCI)** technology and **Eye Tracking** to personalize education for neurodiverse students — particularly those with **ADHD**.

Traditional education's "one-size-fits-all" model fails the 10–15% of Indian students who have specific learning disabilities. NeuroLearn addresses this by listening directly to the brain. When a student's attention drops, the system detects it instantly through EEG signals and eye gaze analysis, then reshapes the learning content using an AI engine — before the student even realizes they've lost focus.

The platform integrates four core technologies into a single seamless loop:

- 🧠 **Non-invasive EEG** for real-time brainwave monitoring
- 👁️ **Eye Tracking** for gaze-based focus detection
- 🤖 **Multi-Path Neural Network** for cognitive state classification (96.4% accuracy)
- 💬 **Large Language Models (LLMs)** for dynamic content adaptation

---

## 🎯 The Problem

In India alone:

- Over **11%** of students exhibit symptoms of ADHD
- **10–15%** of students have specific learning disabilities including dyslexia
- Traditional classrooms use **static content** that cannot respond to a student's fluctuating attention
- Teachers have **no real-time visibility** into individual engagement levels
- Manual interventions are **too slow** to match the rapid cognitive shifts of individual learners
- Neurodiverse students face constant **cognitive overload**, low self-esteem, and anxiety in standard learning environments

---

## 💡 The Solution

NeuroLearn is a **closed-loop BCI system** that:

1. **Reads** brainwave signals via a non-invasive EEG headband placed on the forehead
2. **Tracks** the student's eyes using computer vision to monitor gaze and focus behavior
3. **Classifies** cognitive state (focused vs. distracted) in real-time using a custom-trained neural network
4. **Adapts** the learning content dynamically using a Large Language Model (LLM)
5. **Reports** engagement data to both students and teachers through interactive dashboards

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                              │
│   EEG Headband (3-channel)    +    Eye Tracker (Camera)         │
└──────────────────┬──────────────────────────┬───────────────────┘
                   │                          │
                   ▼                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ON-DEVICE PROCESSING                         │
│         Arduino UNO R4  ←→  BioAmp EXG Pill Amplifier          │
│              ADC @ 250 Hz  →  USB Serial Stream                 │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                         AI ENGINE                               │
│  ┌──────────────────┐  ┌─────────────────┐  ┌───────────────┐  │
│  │  Signal Filter   │  │ Eye Gaze Model  │  │  LLM Engine   │  │
│  │  Band-pass       │  │ (Focus/Distract)│  │ (ChatGPT /    │  │
│  │  0.5–30 Hz       │  │                 │  │  Gemini)      │  │
│  │  + Notch Filter  │  │                 │  │               │  │
│  └────────┬─────────┘  └───────┬─────────┘  └──────┬────────┘  │
│           │                    │                    ▲           │
│           ▼                    ▼                    │           │
│  ┌───────────────────────────────────────┐          │           │
│  │    Multi-Path Neural Network          │──────────┘           │
│  │    • Temporal CNN Path (+ Attention)  │  Cognitive State     │
│  │    • Statistical Feature Path         │  Label               │
│  │    • Frequency Feature Path           │                      │
│  └───────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                             │
│       Student Dashboard           Teacher Dashboard             │
│       • Live attention %          • Class-wide view             │
│       • Beta wave live graph      • Per-student status          │
│       • Eye gaze indicator        • PDF report export           │
│       • Adaptive content          • Accessibility controls      │
│       • Quiz interventions                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Hardware Components

<!-- ================================================================ -->
<!-- HARDWARE IMAGE PLACEHOLDERS                                       -->
<!-- To add images: upload your photos to an /assets/images/ folder   -->
<!-- in this repo, then uncomment the img tags below and update paths -->
<!-- ================================================================ -->

### 🎧 EEG Headband (3-Channel)

<!-- ![EEG Headband worn by user](assets/images/eeg_headband.jpg) -->
<img width="600" height="451" alt="image" src="https://github.com/user-attachments/assets/50db769a-b8b6-4652-a839-d0a430b9b029" />

A custom 3-channel EEG band with **two active electrodes on the forehead** (Fp1, Fp2) to capture frontal brain activity relevant to attention, and a **third reference/ground electrode** for noise cancellation. Designed to be lightweight and comfortable for extended study sessions.

---

### 🔬 BioAmp EXG Pill — Signal Amplifier

<!-- ![BioAmp EXG Pill module](assets/images/bioamp_exg_pill.jpg) -->
<img width="630" height="348" alt="image" src="https://github.com/user-attachments/assets/a4032716-4dcb-4c47-9bd8-cec8cd62aed6" />

A compact amplifier module that boosts **microvolt-level EEG signals** to a measurable range. Uses **differential inputs (IN+, IN−)** to measure the voltage difference between electrodes — a technique that cancels out common-mode electrical noise. A **reference electrode (REF)** provides a stable baseline, further improving signal quality.

---

### 🔧 Arduino UNO R4 Minima — Microcontroller

<!-- ![Arduino UNO R4 Minima board](assets/images/arduino_uno_r4.jpg) -->
<img width="735" height="546" alt="image" src="https://github.com/user-attachments/assets/a74aa6ad-adf3-4518-b005-6d6121198d47" />

The bridge between the analog biological world and the digital computational domain. The Arduino's built-in **Analog-to-Digital Converter (ADC)** samples the amplified EEG signal at **250 Hz** and transmits the digital data stream to a laptop over **USB serial** for software-based processing.

---

### 👁️ Eye Tracking Camera Setup

<!-- ![Eye tracking camera setup](assets/images/eye_tracker.jpg) -->

A standard webcam or dedicated IR camera positioned to capture the student's face during sessions. Used for real-time gaze direction detection, blink rate analysis, fixation tracking, and head pose estimation.

---

### 🔌 Full Circuit — EEG Signal Acquisition

<!-- ![EEG circuit diagram](assets/images/circuit_diagram.jpg) -->
<img width="1200" height="585" alt="image" src="https://github.com/user-attachments/assets/56ccb55b-e95e-400c-88a7-3ba6ae9d7932" />

The complete analog front-end circuit connecting the EEG electrodes → BioAmp EXG Pill amplifier → band-pass RC filter stage → Arduino ADC input.

| Component | Specification |
|-----------|---------------|
| **EEG Headband** | 3-channel, Fp1 + Fp2 active, 1 reference/ground |
| **BioAmp EXG Pill** | Differential amplifier, IN+, IN−, REF inputs |
| **Arduino UNO R4** | Built-in ADC, 250 Hz sampling rate, USB output |
| **Eye Tracker** | Standard webcam or IR camera |

> **Scalability:** The 3-channel prototype is designed to expand to a full **19-channel EEG system** (10-20 international standard) for richer spatial brain mapping in future iterations.

---

## 👁️ Eye Tracking Module

Beyond EEG, NeuroLearn integrates a real-time **eye tracking system** that provides a second, independent channel of attention data — making the system significantly more robust, especially in environments where EEG signals may carry more noise.

### What It Tracks

| Signal | How It's Interpreted |
|--------|----------------------|
| **Gaze Direction** | Detects whether the student's eyes are directed at the screen or looking away |
| **Blink Rate** | Elevated or suppressed blink rates indicate fatigue or cognitive stress |
| **Fixation & Saccades** | Long fixations = active reading; rapid random saccades = mind-wandering |
| **Head Pose** | Detects if the student has physically turned away from the learning material |

### Focus Signals — At a Glance

| Cue | Focused | Distracted |
|-----|---------|------------|
| Gaze | Stable, on-screen | Off-axis, wandering |
| Blink Rate | Normal (15–20/min) | Very high or very low |
| Fixations | Long and structured | Short and scattered |
| Head Pose | Forward-facing | Turned away |

### Multimodal Fusion with EEG

Eye tracking data is **fused with EEG brainwave features** before being passed into the classifier. When both modalities independently signal distraction, the system's confidence in triggering an intervention is much higher. This fusion approach:

- Reduces **false positives** — a student thinking deeply with eyes briefly unfocused won't be interrupted
- Improves **reliability** in noisy real-world settings where EEG alone may be less stable
- Provides a richer, multi-dimensional picture of the student's cognitive state

---

## 🤖 Machine Learning Model

### Architecture — Multi-Path Neural Network

The model processes EEG data through **three parallel paths** and merges their outputs:

```
Raw EEG Signal
      │
      ├──► Path 1: Temporal CNN
      │    Conv1D → BatchNorm → MaxPool → Dropout → Attention Mechanism
      │    (learns patterns directly from the raw time-series waveform)
      │
      ├──► Path 2: Statistical Features
      │    Linear Layer
      │    (processes mean, variance, skewness, kurtosis, etc.)
      │
      └──► Path 3: Frequency Features
           Linear Layer
           (processes Alpha, Beta, Theta band power values)
                │
                ▼
          Concatenation of all three feature vectors
                │
                ▼
          Sigmoid Output → Probability Score
          FOCUSED  |  DISTRACTED
```

The **Attention Mechanism** in Path 1 is a key architectural innovation — it dynamically assigns higher weight to the time segments within the EEG window that are most diagnostic of the student's cognitive state, closely mimicking how a clinician would read a brainwave trace.

### Training & Validation

- Validation method: **5-Fold Cross-Validation**
- Classification target: Binary — `FOCUSED` vs. `DISTRACTED`

### Performance Results

| Metric | Score | What It Means |
|--------|-------|---------------|
| **Accuracy** | **96.4%** | Correct classification in 96.4% of all test cases |
| **Precision** | 97.0% | When the model flags "distracted," it is correct 97% of the time |
| **Recall** | 98.0% | Catches 98% of all actual distraction events — very few missed |
| **F1-Score** | 93.27% | Balanced harmonic measure of precision and recall |
| **AUC** | 0.99 | Near-perfect discriminative power (1.0 = perfect) |

**Cross-Validation Breakdown:**

```
Fold 1:  Accuracy 0.9700  |  F1: 0.9487
Fold 2:  Accuracy 0.9750  |  F1: 0.9693  ← Best Fold
Fold 3:  Accuracy 0.9650  |  F1: 0.8977
Fold 4:  Accuracy 0.9700  |  F1: 0.9357
Fold 5:  Accuracy 0.9400  |  F1: 0.9123
──────────────────────────────────────────
Mean Accuracy :  0.9640  ±  0.0124
Mean F1 Score :  0.9327  ±  0.0255
```

> A **Recall of 98%** means the system misses fewer than 2 in 100 distraction events — ensuring interventions are timely and effective.

---

## 📡 EEG Signal Processing Pipeline

```
Raw Signal  ──►  Arduino ADC (250 Hz sampling)
                        │
                        ▼
           Band-pass Filter  [0.5 Hz – 30 Hz]
           Removes slow baseline drift and high-frequency muscle noise
                        │
                        ▼
           Notch Filter  [50 Hz / 60 Hz]
           Eliminates power line electrical interference
                        │
                        ▼
           Feature Extraction from EEG Frequency Bands
           ┌──────────────────────────────────────────────────┐
           │  Alpha  [8–13 Hz]  →  Low alpha  =  attentive    │
           │  Beta   [13–30 Hz] →  High frontal beta = focused │
           │  Theta  [4–8 Hz]   →  High theta = drowsy/loaded  │
           └──────────────────────────────────────────────────┘
                        │
                        ▼
           Multi-Path Neural Network Classifier
                        │
                        ▼
               FOCUSED  |  DISTRACTED
```

**Key pattern:** High frontal Beta + Low frontal Alpha → attentive state.
High parietal Alpha → distracted or disengaged state.

---

## 🔄 The Adaptive Loop

```
Student logs in & connects EEG + Eye Tracker
                    │
                    ▼
          Select subject & content format
                    │
                    ▼
     ┌─────── Monitor EEG + Gaze in real-time ◄──────────────┐
     │                     │                                  │
     │                     ▼                                  │
     │             Attention Low?                             │
     │             │          │                               │
     │            YES         NO ──► Continue Studying ───────┤
     │             │                                          │
     │             ▼                                          │
     │      Show Focus Alert Pop-up                           │
     │             │                                          │
     │      3+ Consecutive Alerts?                            │
     │             │          │                               │
     │            YES         NO ─────────────────────────────┘
     │             │
     │             ▼
     │    Trigger Interactive Quiz
     │    OR  LLM reformats content into:
     │         • Concise summary
     │         • Key questions
     │         • Simplified step-by-step breakdown
     └────────────────────────────────────────────────────────┘
                    │
          Module Complete?
                    │
                    ▼
     Final Test  →  Generate Session Report
```

---

## 🧩 Platform Features

### Student Dashboard

| Feature | Description |
|---------|-------------|
| 📊 **Live Attention Score** | Real-time percentage display of current focus level |
| 📈 **Beta Wave Graph** | Live visualization of brainwave activity correlated to focus |
| 👁️ **Eye Gaze Indicator** | Visual cue showing whether the student's gaze is currently on-screen |
| 🔥 **Focus Streak** | Gamified counter of consecutive focused minutes |
| 📚 **Content Format Selection** | Choose from video, article, or interactive quiz |
| 🕹️ **Session & Quiz History** | Review all past sessions and track progress over time |
| 🟡 **Focus Alerts** | Gentle, non-disruptive pop-up when attention drops below threshold |
| 🧩 **Auto Quiz Intervention** | Short interactive quiz auto-triggered after 3+ low-attention alerts |
| 📝 **Post-Session Insight** | Attention timeline graph + personalized feedback for self-reflection |

### Teacher Dashboard

| Feature | Description |
|---------|-------------|
| 📊 **Class Attention Overview** | Live average attention rate across all students in the session |
| 👤 **Per-Student Status** | Real-time "Focused / Distracted" badge for every student |
| 📄 **PDF Report Export** | Detailed session reports for deeper analysis or parent-teacher meetings |
| ♿ **Accessibility Controls** | Dyslexia-friendly fonts, letter spacing, font size, light/dark themes |
| 🤖 **Model Info** | Displays which ML model is active and its current accuracy |

---

## 📚 Theoretical Foundation

| Theory | How NeuroLearn Applies It |
|--------|--------------------------|
| **Cognitive Load Theory** (Sweller, 1988) | Content is dynamically reformatted to reduce extraneous cognitive load the moment overload is detected |
| **Zone of Proximal Development** (Vygotsky) | System keeps each student within their optimal cognitive challenge zone — neither bored nor overwhelmed |
| **Passive BCI Paradigm** (Zander & Kothe, 2011) | Brainwave data is used as implicit, continuous input — no deliberate user action is required |

---

## 🗺️ Research Gaps Addressed

| Gap in Existing Literature | NeuroLearn's Approach |
|---------------------------|----------------------|
| BCI adaptation systems overlook motivation | Gamified elements (Focus Streak, quizzes) serve as built-in motivational catalysts |
| No tailored tools for both ADHD and dyslexia | Dyslexia-friendly fonts, ADHD-aware pacing, and LLM-driven content simplification |
| Few EEG channels miss the full cognitive picture | Scalable from 3-channel prototype → full 19-channel system |
| Adaptive systems only adjust difficulty | LLM reshapes content *format* (quiz, summary, key questions) — not just difficulty level |
| EEG alone misses behavioral attention cues | Eye tracking fused with EEG for multimodal, more reliable detection |

---

## 🔭 Future Roadmap

- [ ] Expand to **19-channel EEG** (10-20 standard) for richer spatial brain activity mapping
- [ ] Transition to **CNN-based classifiers** for better generalization across different individuals
- [ ] Integrate **Heart Rate Variability (HRV)** and **Electrodermal Activity (EDA)** as additional physiological signals
- [ ] Add **auditory explanations** and **visual analogy generation** via LLM for different learner types
- [ ] Upgrade eye tracking to dedicated **IR-based hardware** for sub-millimeter gaze precision
- [ ] Conduct **longitudinal pilot studies** in diverse real-world school settings across India
- [ ] Seamless integration with **Google Classroom** and **Moodle** LMS platforms

---

## ⚠️ Current Limitations

- Model trained on a curated dataset — needs validation on a larger, more diverse student population including those with formal ADHD and dyslexia diagnoses
- All testing conducted in controlled lab settings; robustness in real-world noisy classrooms not yet fully characterized
- Binary (focused/distracted) classification is a simplification — future versions will support multi-level attention scoring for finer-grained adaptations
- Long-term learning outcome impact not yet measured over a full academic term

---

## 📺 Demo Video

<!-- ================================================================ -->
<!-- YOUTUBE VIDEO PLACEHOLDER                                         -->
<!-- Replace YOUR_VIDEO_ID below with your actual YouTube video ID    -->
<!-- e.g. if your URL is https://www.youtube.com/watch?v=dQw4w9WgXcQ -->
<!--      then YOUR_VIDEO_ID = dQw4w9WgXcQ                            -->
<!-- ================================================================ -->

[![NeuroLearn Demo](<img width="1909" height="739" alt="image" src="https://github.com/user-attachments/assets/6571a97e-1c08-4277-9bac-c70b13bbea00" />
)](https://youtu.be/5Z5D2E9MgPA)

---

## 🏛️ Alignment with National Policy

NeuroLearn aligns with India's **National Education Policy (NEP)** by:
- Promoting **inclusive education** for every learner regardless of neurotype
- Supporting **EdTech innovation** as a national priority
- Reducing dependence on expensive, hard-to-access specialized tutoring
- Empowering teachers with objective, data-driven tools for targeted student support

---

*"By creating an environment that responds to each student's unique cognitive patterns, we aim to transform frustration into focus and unlock the full potential of every learner."*
