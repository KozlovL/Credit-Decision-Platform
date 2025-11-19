{{- define "scoring-service.fullname" -}}
{{- .Values.fullnameOverride | default .Chart.Name -}}
{{- end -}}
