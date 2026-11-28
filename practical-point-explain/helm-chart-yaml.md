# `Chart.yaml` — Line-by-Line Explanation (With Real-World Production Examples)

Source file: `/home/shumon/Documents/coding-practice/practical/04-helm-packaging/polyglot-api/Chart.yaml`

## Short Summary (TL;DR)
* **What this file does:** Defines the metadata and identity of the Helm chart itself (`apiVersion: v2` for Helm 3, `name: polyglot-api`, `type: application`, chart `version: 0.1.0`, and `appVersion: "1.0.1"`), which Helm reads to package, publish, and populate `.Chart.Name` and `.Chart.Version` in templates like `_helpers.tpl`.
* **Why it is needed:** `Chart.yaml` is **mandatory** for every Helm chart—without it, Helm does not recognize the directory as a chart and `helm install` / `helm package` / `helm lint` will fail.
* **Real-world production example:** When pushing charts to an OCI registry or ChartMuseum (`helm package` $\rightarrow$ `polyglot-api-0.1.0.tgz`), teams bump `version` (`0.1.0` $\rightarrow$ `0.1.1`) whenever Kubernetes templates change, and bump `appVersion` (`"1.0.1"` $\rightarrow$ `"1.0.2"`) when the application release changes—making rollbacks (`helm rollback polyglot-api 1`) clean and traceable.

---

## Exact File

```yaml
apiVersion: v2
name: polyglot-api
description: Production-grade Helm chart for node-api, python-api, and go-api
type: application
version: 0.1.0
appVersion: "1.0.1"
```

---

## Line-by-Line Breakdown

### Line 1: `apiVersion: v2`
* **What `apiVersion` means (here):** The **Helm Chart API version** (not a Kubernetes resource `apiVersion`!).
* **What `v2` means:** **Helm 3** format (supports `type:` and `dependencies:` directly in `Chart.yaml`; Helm 2 used `v1`).
* **Without it:** `helm lint` / `helm install` fails because `apiVersion` is required.

### Line 2: `name: polyglot-api`
* **What `name` means:** The official name of the Helm chart.
* **Where it is used:**
  * Populates `{{ .Chart.Name }}` in `_helpers.tpl` (`helm.sh/chart: polyglot-api-0.1.0`).
  * Becomes the package filename when running `helm package`: `polyglot-api-0.1.0.tgz`.
* **Real-world production example:** Must use lowercase letters, numbers, and hyphens (`polyglot-api`), matching the folder name by convention.

### Line 3: `description: Production-grade Helm chart for node-api, python-api, and go-api`
* **What it means:** Human-readable summary shown when running `helm search repo` or `helm show chart`.

### Line 4: `type: application`
* **What `type` means:** Tells Helm what kind of chart this is. There are only two valid values:
  * **`application`** (default): A deployable chart that creates Kubernetes resources (`Deployment`, `Service`, `Ingress`, etc.) via `helm install`.
  * **`library`**: A reusable helper-only chart (contains only `_*.tpl` partials, no deployable K8s resources, used as a dependency by other charts).
* **Real-world production example:** Large companies have 1 `company-common` **`library`** chart for standard labels/probes, and many **`application`** charts for each service.

### Line 5: `version: 0.1.0`
* **What `version` means:** The **SemVer 2 version of the Helm chart itself** (`MAJOR.MINOR.PATCH`).
* **Where it is used:** Populates `{{ .Chart.Version }}` in `_helpers.tpl` and versions the `.tgz` package in registries.
* **Real-world production example:** Every time you edit `templates/deployments.yaml` or `values.yaml`, you **must** bump `version` (`0.1.0` $\rightarrow$ `0.1.1`) before pushing to an OCI/Helm registry, because registries reject overwriting an existing chart version.

### Line 6: `appVersion: "1.0.1"`
* **What `appVersion` means:** Informational version of the **application** packaged by this chart (stored as a quoted string).
* **Why `version` and `appVersion` are separate:** You might fix a typo in `ingress.yaml` (bump `version` to `0.1.1` while `appVersion` stays `"1.0.1"`), or release a new app build (bump `appVersion` to `"1.0.2"`).
* **Why it is quoted (`"1.0.1"`):** SemVer/calver strings or versions like `"1.0"` can be misread as floats by YAML parsers if unquoted, so Helm best practice always quotes `appVersion`.
