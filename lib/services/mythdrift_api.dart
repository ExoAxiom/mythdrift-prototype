import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class MythdriftApi {
  // Configure for your environment:
  //   Physical device on LAN  → your machine's LAN IP, e.g. 192.168.x.x
  //   Android emulator        → 10.0.2.2
  //   iOS simulator / desktop → localhost
  static const String _baseUrl = "http://localhost:5000";
  static const String _narratorsCacheKey = 'mythdrift_narrators_cache';

  static Future<Map<String, dynamic>> createSession(String narrator) async {
    final response = await http.post(
      Uri.parse("$_baseUrl/session"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"narrator": narrator}),
    );
    if (response.statusCode == 200) return jsonDecode(response.body);
    throw Exception("Failed to create session: ${response.statusCode}");
  }

  static Future<Map<String, dynamic>?> loadSession(String sessionId) async {
    final response = await http.get(Uri.parse("$_baseUrl/session/$sessionId"));
    if (response.statusCode == 200) return jsonDecode(response.body);
    if (response.statusCode == 404) return null;
    throw Exception("Failed to load session: ${response.statusCode}");
  }

  /// Returns (narrators, fromCache) — fromCache=true means backend was unreachable.
  static Future<(List<Map<String, dynamic>>, bool)> getNarrators() async {
    try {
      final response = await http
          .get(Uri.parse("$_baseUrl/narrators"))
          .timeout(const Duration(seconds: 5));
      if (response.statusCode == 200) {
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString(_narratorsCacheKey, response.body);
        final data = jsonDecode(response.body);
        return (List<Map<String, dynamic>>.from(data["narrators"]), false);
      }
      throw Exception("Status ${response.statusCode}");
    } catch (_) {
      final prefs = await SharedPreferences.getInstance();
      final cached = prefs.getString(_narratorsCacheKey);
      if (cached != null) {
        final data = jsonDecode(cached);
        return (List<Map<String, dynamic>>.from(data["narrators"]), true);
      }
      rethrow;
    }
  }

  static Future<List<Map<String, dynamic>>> getSessions() async {
    final response = await http.get(Uri.parse("$_baseUrl/sessions"));
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return List<Map<String, dynamic>>.from(
        (data["sessions"] as List).map((e) => Map<String, dynamic>.from(e)),
      );
    }
    throw Exception("Failed to load sessions: ${response.statusCode}");
  }

  static Future<Map<String, dynamic>> sendChoice({
    required List<Map<String, dynamic>> history,
    required String playerChoice,
    required String narrator,
    required String currentBeatId,
    String? sessionId,
  }) async {
    final body = {
      "history": history,
      "player_choice": playerChoice,
      "narrator": narrator,
      "current_beat_id": currentBeatId,
      if (sessionId != null) "session_id": sessionId,
    };
    final response = await http.post(
      Uri.parse("$_baseUrl/mythdrift"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(body),
    );
    if (response.statusCode == 200) return jsonDecode(response.body);
    throw Exception(
      "Mythdrift backend error: ${response.statusCode} — ${response.body}",
    );
  }
}
