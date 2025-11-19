{{- define "flow-selection-service.fullname" -}}
{{- .Values.fullnameOverride | default .Chart.Name -}}
{{- end -}}
