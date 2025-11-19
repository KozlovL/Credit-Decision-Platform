{{- define "user-data-service.fullname" -}}
{{- .Values.fullnameOverride | default .Chart.Name -}}
{{- end -}}
