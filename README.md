# 🚀 Kubernetes HPA Lab — Load Testing, Autoscaling & Observability

![Kubernetes](https://img.shields.io/badge/Kubernetes-1.35-326CE5?logo=kubernetes\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask\&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?logo=prometheus\&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Visualization-F46800?logo=grafana\&logoColor=white)
![k6](https://img.shields.io/badge/k6-Load%20Testing-7D64FF?logo=k6\&logoColor=white)
![Minikube](https://img.shields.io/badge/Minikube-Local%20Kubernetes-2D3748?logo=kubernetes\&logoColor=white)

## 📖 Overview

This project is a hands-on Kubernetes lab focused on **Horizontal Pod Autoscaling (HPA), load testing, and observability**.

I built a small containerized Flask application and deployed it to a local Kubernetes cluster using **Minikube**. The application was configured with resource requests and limits, liveness and readiness probes, and an HPA based on CPU utilization.

I then used **k6** to generate increasing HTTP traffic against the application and observed Kubernetes automatically increase and decrease the number of application pods based on CPU utilization.

For monitoring, I deployed **Prometheus and Grafana using kube-prometheus-stack** to observe application CPU usage, pod count, HPA behavior, and Kubernetes metrics.

The main goal of the project was to understand how these Kubernetes components work together during a real workload:

---

## 🎯 What I Built

* Containerized a Python Flask application using Docker
* Deployed the application to Kubernetes using Minikube
* Created a dedicated Kubernetes namespace for the project
* Configured Kubernetes Deployment and Service resources
* Added liveness and readiness probes
* Configured CPU and memory resource requests and limits
* Enabled Kubernetes Metrics Server
* Configured a Horizontal Pod Autoscaler using CPU utilization
* Created a k6 load-testing Job running inside the Kubernetes cluster
* Installed Prometheus and Grafana using `kube-prometheus-stack`
* Created Grafana panels to visualize HPA and application behavior
* Tested application health and readiness behavior
* Observed Kubernetes scaling pods under CPU load and scaling them back down after the load stopped

---

## 🏗️ Architecture

<p align="center">
  <img width="1672" height="941" alt="k8-d1" src="https://github.com/user-attachments/assets/954a207a-8605-4cac-aeaa-be02ec0b2429" />
</p>

The project runs primarily inside a **Minikube cluster**.

The Flask application runs as Kubernetes Pods behind a ClusterIP Service. The k6 load-testing Job generates traffic through the Service.

The HPA uses CPU utilization metrics provided by **Metrics Server** to adjust the desired replica count of the Flask Deployment.

Prometheus collects Kubernetes and node/application-related metrics, while Grafana provides dashboards for visualizing the system.

---

---

## 🏗️ Screenshots
<img width="858" height="427" alt="ss3" src="https://github.com/user-attachments/assets/af96b8d6-22a5-47be-bc81-e3daeb2285f0" />
<img width="1918" height="867" alt="ss2" src="https://github.com/user-attachments/assets/f4675173-9729-44ea-85af-d920a94374ce" />
<img width="1918" height="868" alt="ss1" src="https://github.com/user-attachments/assets/af48694a-0dad-4a64-a5cb-189095c6447d" />
<img width="1231" height="271" alt="ss4" src="https://github.com/user-attachments/assets/3b4e8378-86ed-4259-bde7-487cf542769b" />



---



## 📁 Repository Structure

```text
k8s-hpa-lab/
├── app/
│   ├── app.py
│   └── requirements.txt
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
│   └── k6-job.yml
├── k6/
│   └── load-test.js
├── Dockerfile
└── README.md
```

---

## 🧰 Technology Stack

| Category              | Technologies                              |
| --------------------- | ----------------------------------------- |
| Application           | Python 3.12, Flask                        |
| Containerization      | Docker                                    |
| Kubernetes            | Kubernetes, Minikube, kubectl             |
| Autoscaling           | Horizontal Pod Autoscaler, Metrics Server |
| Load Testing          | Grafana k6                                |
| Monitoring            | Prometheus                                |
| Visualization         | Grafana                                   |
| Kubernetes Monitoring | kube-prometheus-stack                     |
| Cloud                 | Amazon EKS / ECR *(planned)*              |

---

## 🐍 Application

The application is intentionally small because the focus of this project is Kubernetes behavior rather than application development.

It provides:

| Endpoint         | Purpose                                         |
| ---------------- | ----------------------------------------------- |
| `/`              | Basic application response                      |
| `/healthz`       | Liveness health check                           |
| `/readyz`        | Readiness health check                          |
| `/work`          | CPU-intensive workload used during load testing |
| `/toggle/health` | Test liveness probe behavior                    |
| `/toggle/ready`  | Test readiness probe behavior                   |

The `/work` endpoint performs CPU-intensive work so that increasing HTTP traffic produces measurable CPU utilization inside the Kubernetes Pods.

---

## ☸️ Kubernetes Deployment

The Flask application was deployed with:

* Initial replica count of **1**
* Container port **5000**
* Liveness probe
* Readiness probe
* CPU request: **100m**
* CPU limit: **300m**
* Memory request: **128Mi**
* Memory limit: **256Mi**
* `ClusterIP` Service for internal communication

The application was isolated inside the `hpa-lab` namespace.

---

## 📈 Horizontal Pod Autoscaling

The project uses a Kubernetes **Horizontal Pod Autoscaler (HPA v2)**.

Configuration:

| Setting          | Value            |
| ---------------- | ---------------- |
| Minimum replicas | 1                |
| Maximum replicas | 5                |
| CPU target       | 50%              |
| Target           | Flask Deployment |

The HPA was tested by generating increasing CPU load against the `/work` endpoint.

The experiment demonstrated the relationship between:

```text
HTTP Load
    ↓
CPU Usage
    ↓
Metrics Server
    ↓
HPA
    ↓
Deployment Replica Count
    ↓
More / Fewer Pods
```

---

## 🧪 Load Testing with k6

I created a k6 load-testing script and ran it inside Kubernetes as a **Job**.

The test progressively increased the number of virtual users and repeatedly accessed the CPU-intensive `/work` endpoint.

### Load Test Stages

| Stage          | Duration | Virtual Users |
| -------------- | -------- | ------------- |
| Warm-up        | 30s      | 5             |
| Ramp-up        | 1m       | 30            |
| Sustained load | 3m       | 60            |
| Cool-down      | 1m       | 10            |
| Stop           | 30s      | 0             |

Running the load test inside Kubernetes allowed k6 to communicate directly with the application's ClusterIP Service.

---

## 📊 Monitoring & Observability

For observability, I deployed **kube-prometheus-stack** into a separate `monitoring` namespace.

The monitoring stack included:

* Prometheus
* Grafana
* Alertmanager
* kube-state-metrics
* node-exporter

This allowed me to observe both Kubernetes resources and the behavior of the HPA during the load test.

### Prometheus

Prometheus was used to query metrics related to:

* Flask Pod count
* Flask Ready Pods count 
* CPU per pod
* Memory usage
* Ready Pods
* HPA current replicas
* HPA desired replicas

<img width="1918" height="868" alt="ss1" src="https://github.com/user-attachments/assets/725af5c8-4537-46a5-8eb6-15663451b75d" />


### Grafana

Grafana was connected to Prometheus and used to visualize the experiment.

The dashboard included panels for:

* Flask Pod count
* Ready Pod count
* CPU usage per Pod
* Memory usage per Pod
* HPA current replicas
* HPA desired replicas
* HPA CPU utilization

---

## 📈 Autoscaling Experiment

The main experiment was performed by starting with a single Flask Pod and gradually increasing HTTP traffic.

The observed behavior followed this pattern:

```text
Low Load
   │
   ▼
1 Pod
   │
   │  k6 generates CPU load
   ▼
CPU utilization increases
   │
   ▼
HPA detects CPU above target
   │
   ▼
Deployment increases replicas
   │
   ▼
Multiple Flask Pods
   │
   │  Load continues
   ▼
HPA can scale up to 5 Pods
```

After the k6 test completed:

```text
Load stops
   │
   ▼
CPU utilization decreases
   │
   ▼
HPA scales replicas down
   │
   ▼
Application returns to minimum replicas
```

This provided a practical demonstration of Kubernetes automatically adjusting application capacity according to workload.

---

## ❤️ Health & Readiness Testing

I also tested the difference between Kubernetes **liveness** and **readiness** probes.

### Readiness

When the readiness check was intentionally failed, the Pod was removed from the Service endpoints while the container continued running.

This demonstrated that readiness controls whether a Pod should receive traffic.

### Liveness

When the liveness check was intentionally failed, Kubernetes detected the unhealthy container and restarted it.

This demonstrated that liveness is used to determine whether a container should be restarted.

---

## 🔍 What I Observed

During the lab, I was able to observe several Kubernetes behaviors directly:

* CPU utilization increased as k6 traffic increased
* HPA reacted to CPU utilization above the configured target
* The Deployment created additional Pods during high load
* Newly created Pods became Ready before receiving Service traffic
* Pod count decreased after the load test finished
* Prometheus collected Kubernetes metrics from the cluster
* Grafana provided a visual representation of CPU usage and autoscaling
* Readiness failures removed Pods from Service endpoints
* Liveness failures caused containers to restart
* Metrics Server provided the resource metrics required by HPA

---

## 🖥️ Running Environment

The main implementation was completed locally using:

* Windows 11
* Docker Desktop
* Minikube
* Kubernetes
* kubectl
* Helm

The project was intentionally developed locally first to experiment with Kubernetes without incurring cloud infrastructure costs.

---

## ☁️ Planned AWS Deployment

After completing the local Minikube implementation, the next stage is to reproduce the experiment on **Amazon EKS** as a short-lived AWS lab.

The planned AWS environment will use:

* Amazon EKS
* Amazon ECR
* Kubernetes HPA
* Metrics Server
* Prometheus
* Grafana

The application image will be stored in Amazon ECR and deployed to an EKS cluster.

The EKS environment will be created temporarily for testing and removed after the experiment to control AWS costs.

---

## 🚀 Future Improvements

* Deploy the application to Amazon EKS
* Store the Docker image in Amazon ECR
* Add Kubernetes Ingress
* Add application-level Prometheus metrics
* Add Grafana alerts
* Add Kubernetes manifests managed through Helm
* Experiment with different HPA targets and scaling policies
