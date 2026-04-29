import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:flutter_tts/flutter_tts.dart';
import 'services/mythdrift_api.dart';
import 'screens/session_history_screen.dart';

class PrototypeScreen extends StatefulWidget {
  final String narrator;
  final String? sessionId;
  final List<Map<String, dynamic>>? initialHistory;
  final String? initialBeatId;
  final List<String>? initialChoices;

  const PrototypeScreen({
    super.key,
    required this.narrator,
    this.sessionId,
    this.initialHistory,
    this.initialBeatId,
    this.initialChoices,
  });

  @override
  State<PrototypeScreen> createState() => _PrototypeScreenState();
}

class _PrototypeScreenState extends State<PrototypeScreen> {
  final FlutterTts _tts = FlutterTts();
  final stt.SpeechToText _speech = stt.SpeechToText();

  String _narratorOutput = "Press Begin to start your drift.";
  List<String> _choices = [];
  List<Map<String, dynamic>> _storyHistory = [];
  String _currentBeatId = "intro";
  String? _sessionId;
  Map<String, double> _mood = {"trust": 0, "suspicion": 0, "curiosity": 0};
  String _driftSignature = "The Drifter";
  String? _lastChoice;
  int _sessionCount = 1;

  bool _isListening = false;
  bool _isLoading = false;
  bool _started = false;
  bool _moodVisible = false;
  bool _isDriftComplete = false;
  bool _hasError = false;

  @override
  void initState() {
    super.initState();
    if (widget.initialHistory != null) {
      _storyHistory = List.from(widget.initialHistory!);
      _currentBeatId = widget.initialBeatId ?? "intro";
      _sessionId = widget.sessionId;
      _started = true;
      _moodVisible = _storyHistory.isNotEmpty;
      if (_storyHistory.isNotEmpty) {
        _narratorOutput = _storyHistory.last['narrator_beat'] as String? ?? '';
      }
      _choices = widget.initialChoices ?? [];
    }
  }

  Future<void> _startAdventure() async {
    setState(() {
      _isLoading = true;
      _isDriftComplete = false;
      _hasError = false;
      _storyHistory = [];
      _currentBeatId = "intro";
      _choices = [];
      _mood = {"trust": 0, "suspicion": 0, "curiosity": 0};
      _moodVisible = false;
    });

    // Only create a new session if we don't already have one
    if (_sessionId == null) {
      try {
        final session = await MythdriftApi.createSession(widget.narrator);
        _sessionId = session['session_id'] as String;
        _sessionCount = (session['session_count'] as int?) ?? 1;
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('mythdrift_session_id', _sessionId!);
      } catch (_) {
        // Continue without persistence
      }
    }

    const opening = "A faint hum stirs the air... your journey begins.";
    const openingChoices = ["step through", "pull back", "speak to the light"];

    _storyHistory.add({
      "player_choice": "start",
      "beat_id": "intro",
      "narrator_beat": opening,
    });

    setState(() {
      _narratorOutput = opening;
      _choices = openingChoices;
      _started = true;
      _isLoading = false;
    });

    await _tts.speak(opening);
  }

  Future<void> _sendChoiceToBackend(String choice) async {
    setState(() {
      _isLoading = true;
      _hasError = false;
      _lastChoice = choice;
    });

    try {
      final data = await MythdriftApi.sendChoice(
        history: _storyHistory,
        playerChoice: choice,
        narrator: widget.narrator,
        currentBeatId: _currentBeatId,
        sessionId: _sessionId,
      );

      final nextBeat = data["next_beat"] as String;
      final nextChoices = List<String>.from(data["choices"] as List);
      final nextBeatId = data["next_beat_id"] as String;
      final rawMood = data["mood"] as Map<String, dynamic>;
      final sig = data["drift_signature"] as String? ?? _driftSignature;

      _storyHistory.add({
        "player_choice": choice,
        "beat_id": nextBeatId,
        "narrator_beat": nextBeat,
      });

      setState(() {
        _narratorOutput = nextBeat;
        _choices = nextChoices;
        _currentBeatId = nextBeatId;
        _mood = rawMood.map((k, v) => MapEntry(k, (v as num).toDouble()));
        _driftSignature = sig;
        _isLoading = false;
        _moodVisible = true;
        if (nextBeatId == "drift_end") _isDriftComplete = true;
      });

      await _tts.speak(nextBeat);
    } catch (e) {
      setState(() {
        _hasError = true;
        _isLoading = false;
        _narratorOutput = "The drift was interrupted.";
      });
    }
  }

  Future<void> _listenForChoice() async {
    bool available = await _speech.initialize();
    if (!available) return;
    setState(() => _isListening = true);
    _speech.listen(
      onResult: (result) {
        if (result.finalResult) {
          setState(() => _isListening = false);
          _sendChoiceToBackend(result.recognizedWords);
        }
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        iconTheme: const IconThemeData(color: Colors.white54),
        title: Column(
          children: [
            Text(
              widget.narrator.toUpperCase(),
              style: const TextStyle(
                color: Colors.white54,
                fontSize: 13,
                letterSpacing: 3,
                fontWeight: FontWeight.w300,
              ),
            ),
            if (_moodVisible) _MoodIndicator(mood: _mood),
          ],
        ),
        centerTitle: true,
      ),
      body: _isDriftComplete
          ? _buildDriftComplete()
          : _buildStoryBody(),
    );
  }

  Widget _buildStoryBody() {
    return Column(
      children: [
        Expanded(
          child: Container(
            padding: const EdgeInsets.all(24),
            alignment: Alignment.topLeft,
            child: SingleChildScrollView(
              child: _isLoading
                  ? const Center(
                      child: Padding(
                        padding: EdgeInsets.only(top: 48),
                        child: CircularProgressIndicator(color: Colors.white38),
                      ),
                    )
                  : Text(
                      _narratorOutput,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        height: 1.6,
                      ),
                    ),
            ),
          ),
        ),

        // Error retry
        if (_hasError && !_isLoading)
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
            child: OutlinedButton(
              style: OutlinedButton.styleFrom(
                foregroundColor: Colors.white54,
                side: const BorderSide(color: Colors.white24),
              ),
              onPressed: _lastChoice != null
                  ? () => _sendChoiceToBackend(_lastChoice!)
                  : null,
              child: const Text("Try again"),
            ),
          ),

        if (_started && !_isLoading && !_hasError && _choices.isNotEmpty)
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: _buildChoiceButtons(),
          ),

        // Bottom controls row
        Stack(
          alignment: Alignment.center,
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 20),
              child: !_started
                  ? ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.white,
                        foregroundColor: Colors.black,
                        padding: const EdgeInsets.symmetric(
                            horizontal: 32, vertical: 14),
                      ),
                      onPressed: _startAdventure,
                      child: const Text("Begin Drift"),
                    )
                  : IconButton(
                      icon: Icon(
                        _isListening ? Icons.mic : Icons.mic_none,
                        color: _isListening ? Colors.white : Colors.white38,
                        size: 32,
                      ),
                      onPressed: _isLoading ? null : _listenForChoice,
                    ),
            ),
            if (_started)
              Positioned(
                right: 20,
                bottom: 20,
                child: Text(
                  "drift #$_sessionCount",
                  style: const TextStyle(
                    color: Colors.white24,
                    fontSize: 10,
                    letterSpacing: 1,
                  ),
                ),
              ),
          ],
        ),
      ],
    );
  }

  Widget _buildDriftComplete() {
    return Padding(
      padding: const EdgeInsets.all(32),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            _narratorOutput,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 18,
              height: 1.6,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 32),
          Text(
            "— $_driftSignature —",
            style: const TextStyle(
              color: Colors.white38,
              fontSize: 13,
              letterSpacing: 2,
              fontWeight: FontWeight.w300,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 48),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.white,
              foregroundColor: Colors.black,
              padding: const EdgeInsets.symmetric(vertical: 14),
            ),
            onPressed: _startAdventure,
            child: const Text("Begin Again"),
          ),
          const SizedBox(height: 12),
          OutlinedButton(
            style: OutlinedButton.styleFrom(
              foregroundColor: Colors.white70,
              side: const BorderSide(color: Colors.white24),
              padding: const EdgeInsets.symmetric(vertical: 14),
            ),
            onPressed: () => Navigator.pop(context),
            child: const Text("Change Narrator"),
          ),
          const SizedBox(height: 12),
          OutlinedButton(
            style: OutlinedButton.styleFrom(
              foregroundColor: Colors.white38,
              side: const BorderSide(color: Colors.white12),
              padding: const EdgeInsets.symmetric(vertical: 14),
            ),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(
                  builder: (_) => const SessionHistoryScreen()),
            ),
            child: const Text("Your Drifts"),
          ),
        ],
      ),
    );
  }

  Widget _buildChoiceButtons() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Padding(
          padding: EdgeInsets.only(bottom: 8),
          child: Text(
            "YOUR MOVE",
            style: TextStyle(
                color: Colors.white24, fontSize: 11, letterSpacing: 2),
          ),
        ),
        ..._choices.map(
          (choice) => Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: OutlinedButton(
              style: OutlinedButton.styleFrom(
                foregroundColor: Colors.white70,
                side: const BorderSide(color: Colors.white24),
                padding: const EdgeInsets.symmetric(vertical: 14),
                alignment: Alignment.centerLeft,
              ),
              onPressed: () => _sendChoiceToBackend(choice),
              child: Padding(
                padding: const EdgeInsets.only(left: 4),
                child: Text(choice, style: const TextStyle(fontSize: 15)),
              ),
            ),
          ),
        ),
      ],
    );
  }
}

class _MoodIndicator extends StatelessWidget {
  final Map<String, double> mood;
  const _MoodIndicator({required this.mood});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 3),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          _MoodDot(label: "curious",   value: mood["curiosity"] ?? 0, activeColor: Colors.blue[200]!),
          const SizedBox(width: 10),
          _MoodDot(label: "trust",     value: mood["trust"] ?? 0,     activeColor: Colors.green[200]!),
          const SizedBox(width: 10),
          _MoodDot(label: "suspicion", value: mood["suspicion"] ?? 0, activeColor: Colors.amber[200]!),
        ],
      ),
    );
  }
}

class _MoodDot extends StatelessWidget {
  final String label;
  final double value;
  final Color activeColor;
  const _MoodDot({required this.label, required this.value, required this.activeColor});

  @override
  Widget build(BuildContext context) {
    final active = value > 0.3;
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(
          active ? Icons.circle : Icons.circle_outlined,
          size: 7,
          color: active ? activeColor : Colors.white24,
        ),
        const SizedBox(width: 3),
        Text(
          label,
          style: TextStyle(
            fontSize: 9,
            letterSpacing: 0.5,
            color: active ? activeColor : Colors.white24,
          ),
        ),
      ],
    );
  }
}
