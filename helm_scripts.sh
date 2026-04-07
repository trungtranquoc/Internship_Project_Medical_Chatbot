$AccountId = "376276261088"
$Region    = "us-east-1"
$Ecr       = "${AccountId}.dkr.ecr.${Region}.amazonaws.com"

aws ecr create-repository --repository-name "thirdparty/csi-secrets-store/driver" --region $Region
aws ecr create-repository --repository-name "thirdparty/csi-secrets-store/driver-crds" --region $Region
aws ecr create-repository --repository-name "thirdparty/sig-storage/csi-node-driver-registrar" --region $Region
aws ecr create-repository --repository-name "thirdparty/sig-storage/livenessprobe" --region $Region

docker buildx imagetools create `
  --tag "${Ecr}/thirdparty/csi-secrets-store/driver:v1.5.6" `
  "registry.k8s.io/csi-secrets-store/driver:v1.5.6"

docker buildx imagetools create `
  --tag "${Ecr}/thirdparty/csi-secrets-store/driver-crds:v1.5.6" `
  "registry.k8s.io/csi-secrets-store/driver-crds:v1.5.6"

docker buildx imagetools create `
  --tag "${Ecr}/thirdparty/sig-storage/csi-node-driver-registrar:v2.13.0" `
  "registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.13.0"

docker buildx imagetools create `
  --tag "${Ecr}/thirdparty/sig-storage/livenessprobe:v2.15.0" `
  "registry.k8s.io/sig-storage/livenessprobe:v2.15.0"


docker buildx imagetools inspect "${Ecr}/thirdparty/csi-secrets-store/driver:v1.5.6"
docker buildx imagetools inspect "${Ecr}/thirdparty/csi-secrets-store/driver-crds:v1.5.6"
docker buildx imagetools inspect "${Ecr}/thirdparty/sig-storage/csi-node-driver-registrar:v2.13.0"
docker buildx imagetools inspect "${Ecr}/thirdparty/sig-storage/livenessprobe:v2.15.0"


helm uninstall csi-secrets-store -n kube-system

helm upgrade --install csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver `
  -n kube-system `
  --set syncSecret.enabled=true `
  --set linux.image.repository="${Ecr}/thirdparty/csi-secrets-store/driver" `
  --set linux.image.tag="v1.5.6" `
  --set linux.image.pullPolicy="Always" `
  --set linux.crds.image.repository="${Ecr}/thirdparty/csi-secrets-store/driver-crds" `
  --set linux.crds.image.tag="v1.5.6" `
  --set linux.crds.image.pullPolicy="Always" `
  --set linux.registrarImage.repository="${Ecr}/thirdparty/sig-storage/csi-node-driver-registrar" `
  --set linux.registrarImage.tag="v2.13.0" `
  --set linux.registrarImage.pullPolicy="Always" `
  --set linux.livenessProbeImage.repository="${Ecr}/thirdparty/sig-storage/livenessprobe" `
  --set linux.livenessProbeImage.tag="v2.15.0" `
  --set linux.livenessProbeImage.pullPolicy="Always" `
  --timeout 10m


helm upgrade csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver `
  -n kube-system `
  --reuse-values `
  --set tokenRequests[0].audience="sts.amazonaws.com" `
  --set tokenRequests[1].audience="pods.eks.amazonaws.com" `
  --timeout 10m




aws ecr create-repository --repository-name "thirdparty/aws-secrets-manager/secrets-store-csi-driver-provider-aws" --region $Region


docker buildx imagetools create `
  --tag "${Ecr}/thirdparty/aws-secrets-manager/secrets-store-csi-driver-provider-aws:3.0.0" `
  "public.ecr.aws/aws-secrets-manager/secrets-store-csi-driver-provider-aws:3.0.0"

docker buildx imagetools inspect "${Ecr}/thirdparty/aws-secrets-manager/secrets-store-csi-driver-provider-aws:3.0.0"

helm repo add aws-secrets-manager https://aws.github.io/secrets-store-csi-driver-provider-aws

helm upgrade --install secrets-provider-aws aws-secrets-manager/secrets-store-csi-driver-provider-aws `
  -n kube-system `
  --set secrets-store-csi-driver.install=false `
  --set image.repository="${Ecr}/thirdparty/aws-secrets-manager/secrets-store-csi-driver-provider-aws" `
  --set image.tag="3.0.0" `
  --set image.pullPolicy="Always" `
  --set awsRegion="us-east-1" `
  --timeout 10m