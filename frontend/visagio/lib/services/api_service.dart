import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiException implements Exception {
  const ApiException(this.message);
  final String message;

  @override
  String toString() => message;
}

class ApiService {
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:5000/api',
  );

  static String? token;
  static bool demoMode = false;
  static int? lastAnalysisId;
  static int? lastRecommendationId;

  static Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      };

  static Future<dynamic> _request(
    String method,
    String path, {
    Map<String, dynamic>? body,
  }) async {
    final uri = Uri.parse('$baseUrl$path');
    late http.Response response;
    try {
      switch (method) {
        case 'GET':
          response = await http.get(uri, headers: _headers);
        case 'POST':
          response = await http.post(uri,
              headers: _headers, body: jsonEncode(body ?? {}));
        case 'PUT':
          response = await http.put(uri,
              headers: _headers, body: jsonEncode(body ?? {}));
        case 'DELETE':
          response = await http.delete(uri, headers: _headers);
        default:
          throw const ApiException('Método HTTP inválido.');
      }
    } on http.ClientException {
      throw const ApiException(
        'Não foi possível conectar à API. Verifique o endereço e o servidor.',
      );
    }

    if (response.statusCode == 204) return null;
    dynamic data;
    try {
      data = response.body.isEmpty ? null : jsonDecode(response.body);
    } on FormatException {
      throw const ApiException('A API retornou uma resposta inválida.');
    }
    if (response.statusCode >= 400) {
      final message = data is Map ? data['message'] : null;
      throw ApiException(message?.toString() ?? 'Não foi possível concluir.');
    }
    return data;
  }

  static Future<Map<String, dynamic>> auth(
    String path,
    Map<String, String> body,
  ) async {
    final data = Map<String, dynamic>.from(
      await _request('POST', '/auth/$path', body: body) as Map,
    );
    token = data['token']?.toString();
    demoMode = false;
    return data;
  }

  static Future<void> savePreferences(
      String hairType, String hairLength) async {
    if (demoMode) return;
    await _request('PUT', '/preferences', body: {
      'hair_type': hairType,
      'hair_length': hairLength,
    });
  }

  static Future<Map<String, dynamic>> createAnalysis({
    String? hairType,
    String? currentLength,
  }) async {
    final data = Map<String, dynamic>.from(
      await _request('POST', '/analyses', body: {
        'face_shape': 'oval',
        'hair_type': hairType ?? 'straight',
        'hair_texture': 'medium',
        'hair_density': 'medium',
        'current_length': currentLength ?? 'medium',
        'score': 95,
        'observations': 'Análise iniciada pelo aplicativo Flutter.',
      }) as Map,
    );
    lastAnalysisId = data['id'] as int?;
    return data;
  }

  static Future<List<Map<String, dynamic>>> generateRecommendations(
    int analysisId,
  ) async {
    final data = await _request(
      'POST',
      '/recommendations/analysis/$analysisId/generate',
    ) as List;
    final items = data.map((item) => Map<String, dynamic>.from(item)).toList();
    if (items.isNotEmpty) lastRecommendationId = items.first['id'] as int?;
    return items;
  }

  static Future<List<Map<String, dynamic>>> recommendations({
    String? category,
  }) async {
    final query = <String>[
      if (lastAnalysisId != null) 'analysis_id=$lastAnalysisId',
      if (category != null) 'category=$category',
    ].join('&');
    final data = await _request(
      'GET',
      '/recommendations${query.isEmpty ? '' : '?$query'}',
    ) as List;
    return data.map((item) => Map<String, dynamic>.from(item)).toList();
  }

  static Future<List<Map<String, dynamic>>> analyses() async {
    final data = await _request('GET', '/analyses') as List;
    return data.map((item) => Map<String, dynamic>.from(item)).toList();
  }

  static Future<void> saveSimulation() async {
    if (demoMode) return;
    if (lastAnalysisId == null) {
      throw const ApiException('Faça uma análise antes de salvar a simulação.');
    }
    await _request('POST', '/simulations', body: {
      'analysis_id': lastAnalysisId,
      'recommendation_id': lastRecommendationId,
      'before_image_url': null,
      'after_image_url': null,
    });
  }

  static Future<List<Map<String, dynamic>>> professionals() async {
    final data = await _request('GET', '/appointments/professionals') as List;
    return data.map((item) => Map<String, dynamic>.from(item)).toList();
  }

  static Future<void> createAppointment({
    required int professionalId,
    required DateTime appointmentDate,
  }) async {
    await _request('POST', '/appointments', body: {
      'professional_id': professionalId,
      'appointment_date': appointmentDate.toIso8601String(),
      'service_name': 'Consultoria de visagismo',
    });
  }
}
