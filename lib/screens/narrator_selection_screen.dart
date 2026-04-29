import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/mythdrift_api.dart';
import '../prototype_screen.dart';
import 'session_history_screen.dart';

class NarratorSelectionScreen extends StatefulWidget {
  const NarratorSelectionScreen({super.key});

  @override
  State<NarratorSelectionScreen> createState() =>
      _NarratorSelectionScreenState();
}

class _NarratorSelectionScreenState extends State<NarratorSelectionScreen>
    with SingleTickerProviderStateMixin {
  List<Map<String, dynamic>> _narrators = [];
  Map<String, dynamic>? _resumeSession;
  bool _isLoading = true;
  bool _isOffline = false;
  String? _error;

  // For skeleton pulse animation
  late final AnimationController _pulseController;
  late final Animation<double> _pulseAnim;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 900),
    )..repeat(reverse: true);
    _pulseAnim = Tween<double>(begin: 0.25, end: 0.55).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );
    _loadAll();
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  Future<void> _loadAll() async {
    setState(() { _isLoading = true; _error = null; _isOffline = false; });
    try {
      final results = await Future.wait([
        MythdriftApi.getNarrators(),
        _checkSavedSession(),
      ]);
      final (narrators, fromCache) = results[0] as (List<Map<String, dynamic>>, bool);
      setState(() {
        _narrators = narrators;
        _resumeSession = results[1] as Map<String, dynamic>?;
        _isLoading = false;
        _isOffline = fromCache;
      });
    } catch (e) {
      setState(() {
        _error = "Could not reach the Mythdrift server.";
        _isLoading = false;
      });
    }
  }

  Future<Map<String, dynamic>?> _checkSavedSession() async {
    final prefs = await SharedPreferences.getInstance();
    final sessionId = prefs.getString('mythdrift_session_id');
    if (sessionId == null) return null;
    try {
      return await MythdriftApi.loadSession(sessionId);
    } catch (_) {
      return null;
    }
  }

  void _selectNarrator(String name) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => PrototypeScreen(narrator: name)),
    );
  }

  void _resumeDrift() {
    final session = _resumeSession!;
    final history = List<Map<String, dynamic>>.from(
      (session['history'] as List).map((e) => Map<String, dynamic>.from(e)),
    );
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => PrototypeScreen(
          narrator: session['narrator'] as String,
          sessionId: session['session_id'] as String,
          initialHistory: history,
          initialBeatId: session['current_beat_id'] as String,
          initialChoices: const [],
        ),
      ),
    );
  }

  String _describeArc(String? arc) {
    switch (arc) {
      case 'the_doorway': return 'The Doorway';
      case 'the_forest':  return 'The Forest';
      case 'the_drift':   return 'The Drift';
      default:            return '';
    }
  }

  // arc from beat_id fallback
  String _arcFromBeatId(String? beatId) {
    if (beatId == null) return '';
    if (beatId.startsWith('forest') || beatId.startsWith('ancient')) return 'The Forest';
    if (beatId.startsWith('doorway') || beatId.startsWith('light') || beatId == 'intro') return 'The Doorway';
    return 'The Drift';
  }

  String _timeSince(String? isoDate) {
    if (isoDate == null || isoDate.isEmpty) return '';
    try {
      final dt = DateTime.parse(isoDate).toLocal();
      final diff = DateTime.now().difference(dt);
      if (diff.inMinutes < 1) return 'just now';
      if (diff.inHours < 1) return '${diff.inMinutes}m ago';
      if (diff.inDays < 1) return '${diff.inHours}h ago';
      return '${diff.inDays}d ago';
    } catch (_) {
      return '';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text(
          "MYTHDRIFT",
          style: TextStyle(
            color: Colors.white,
            letterSpacing: 4,
            fontWeight: FontWeight.w300,
          ),
        ),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.history, color: Colors.white38),
            tooltip: "Your drifts",
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const SessionHistoryScreen()),
            ),
          ),
        ],
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_error != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.wifi_off, color: Colors.white38, size: 48),
              const SizedBox(height: 16),
              Text(
                _error!,
                style: const TextStyle(color: Colors.white54, fontSize: 14),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 24),
              TextButton(
                onPressed: _loadAll,
                child: const Text("Retry", style: TextStyle(color: Colors.white70)),
              ),
            ],
          ),
        ),
      );
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        // Offline banner
        if (_isOffline)
          Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
            color: Colors.amber.withOpacity(0.12),
            child: const Text(
              "⚠  Using cached narrators — server unreachable",
              style: TextStyle(color: Colors.amber, fontSize: 11, letterSpacing: 0.5),
              textAlign: TextAlign.center,
            ),
          ),

        const SizedBox(height: 28),
        const Text(
          "Choose your narrator",
          style: TextStyle(color: Colors.white54, fontSize: 14, letterSpacing: 2),
        ),
        const SizedBox(height: 20),

        Expanded(
          child: _isLoading
              ? _buildSkeleton()
              : ListView(
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 4),
                  children: [
                    if (_resumeSession != null) ...[
                      _ResumeCard(
                        narratorName: _resumeSession!['narrator'] as String? ?? '',
                        arc: _describeArc(_resumeSession!['arc'] as String?) .isNotEmpty
                            ? _describeArc(_resumeSession!['arc'] as String?)
                            : _arcFromBeatId(_resumeSession!['current_beat_id'] as String?),
                        sessionCount: _resumeSession!['session_count'] as int? ?? 1,
                        driftSignature: _resumeSession!['drift_signature'] as String? ?? 'The Drifter',
                        timeSince: _timeSince(_resumeSession!['last_played'] as String?),
                        onTap: _resumeDrift,
                      ),
                      const SizedBox(height: 20),
                      const Padding(
                        padding: EdgeInsets.only(bottom: 12),
                        child: Text(
                          "OR START FRESH",
                          style: TextStyle(color: Colors.white24, fontSize: 11, letterSpacing: 2),
                        ),
                      ),
                    ],
                    ..._narrators.asMap().entries.map((e) => Padding(
                      padding: EdgeInsets.only(bottom: e.key < _narrators.length - 1 ? 12 : 0),
                      child: _NarratorCard(
                        name: e.value["name"] as String,
                        tone: e.value["tone"] as String,
                        behavior: e.value["behavior"] as String,
                        onTap: () => _selectNarrator(e.value["name"] as String),
                      ),
                    )),
                    const SizedBox(height: 24),
                  ],
                ),
        ),
      ],
    );
  }

  Widget _buildSkeleton() {
    return AnimatedBuilder(
      animation: _pulseAnim,
      builder: (context, _) {
        return ListView.separated(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 4),
          itemCount: 3,
          separatorBuilder: (_, __) => const SizedBox(height: 12),
          itemBuilder: (_, __) => Container(
            height: 88,
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(_pulseAnim.value),
              borderRadius: BorderRadius.circular(8),
            ),
          ),
        );
      },
    );
  }
}

class _ResumeCard extends StatelessWidget {
  final String narratorName;
  final String arc;
  final int sessionCount;
  final String driftSignature;
  final String timeSince;
  final VoidCallback onTap;

  const _ResumeCard({
    required this.narratorName,
    required this.arc,
    required this.sessionCount,
    required this.driftSignature,
    required this.timeSince,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.08),
          border: Border.all(color: Colors.white54),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "RESUME DRIFT",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 12,
                      letterSpacing: 2,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    [narratorName, if (arc.isNotEmpty) arc].join(' · '),
                    style: const TextStyle(color: Colors.white70, fontSize: 14),
                  ),
                  Text(
                    'Drift #$sessionCount · $driftSignature',
                    style: const TextStyle(color: Colors.white54, fontSize: 12),
                  ),
                  if (timeSince.isNotEmpty)
                    Text(
                      timeSince,
                      style: const TextStyle(color: Colors.white38, fontSize: 11),
                    ),
                ],
              ),
            ),
            const Icon(Icons.arrow_forward_ios, color: Colors.white38, size: 16),
          ],
        ),
      ),
    );
  }
}

class _NarratorCard extends StatelessWidget {
  final String name;
  final String tone;
  final String behavior;
  final VoidCallback onTap;

  const _NarratorCard({
    required this.name,
    required this.tone,
    required this.behavior,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.05),
          border: Border.all(color: Colors.white24),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(name,
                style: const TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.w500,
                    letterSpacing: 1)),
            const SizedBox(height: 6),
            Text(tone,
                style: const TextStyle(
                    color: Colors.white54,
                    fontSize: 13,
                    fontStyle: FontStyle.italic)),
            const SizedBox(height: 4),
            Text(behavior,
                style: const TextStyle(color: Colors.white38, fontSize: 12)),
          ],
        ),
      ),
    );
  }
}
