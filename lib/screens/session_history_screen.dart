import 'package:flutter/material.dart';
import '../services/mythdrift_api.dart';

class SessionHistoryScreen extends StatefulWidget {
  const SessionHistoryScreen({super.key});

  @override
  State<SessionHistoryScreen> createState() => _SessionHistoryScreenState();
}

class _SessionHistoryScreenState extends State<SessionHistoryScreen> {
  List<Map<String, dynamic>> _sessions = [];
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final sessions = await MythdriftApi.getSessions();
      setState(() {
        _sessions = sessions;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = "$e";
        _isLoading = false;
      });
    }
  }

  String _describeArc(String? beatId) {
    if (beatId == null) return '';
    if (beatId.startsWith('forest') || beatId == 'forest_edge') return 'The Forest';
    if (beatId.startsWith('doorway') || beatId.startsWith('light') || beatId == 'intro') return 'The Doorway';
    if (beatId == 'city_gate' || beatId.startsWith('city') || beatId == 'void_edge' ||
        beatId == 'void_depths' || beatId == 'drift_end' || beatId == 'path_alone') return 'The Drift';
    if (beatId.startsWith('ancient')) return 'The Forest';
    return '';
  }

  String _timeSince(String? isoDate) {
    if (isoDate == null || isoDate.isEmpty) return '';
    try {
      final dt = DateTime.parse(isoDate).toLocal();
      final diff = DateTime.now().difference(dt);
      if (diff.inMinutes < 1) return 'just now';
      if (diff.inHours < 1) return '${diff.inMinutes}m ago';
      if (diff.inDays < 1) return '${diff.inHours}h ago';
      if (diff.inDays == 1) return 'yesterday';
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
        iconTheme: const IconThemeData(color: Colors.white54),
        title: const Text(
          "YOUR DRIFTS",
          style: TextStyle(
            color: Colors.white,
            fontSize: 13,
            letterSpacing: 4,
            fontWeight: FontWeight.w300,
          ),
        ),
        centerTitle: true,
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator(color: Colors.white38));
    }

    if (_error != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.wifi_off, color: Colors.white24, size: 40),
              const SizedBox(height: 16),
              Text(
                "Could not load drift history.",
                style: const TextStyle(color: Colors.white38, fontSize: 14),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              TextButton(
                onPressed: () { setState(() { _isLoading = true; _error = null; }); _load(); },
                child: const Text("Retry", style: TextStyle(color: Colors.white54)),
              ),
            ],
          ),
        ),
      );
    }

    if (_sessions.isEmpty) {
      return const Center(
        child: Text(
          "No drifts yet.",
          style: TextStyle(color: Colors.white38, fontSize: 14, letterSpacing: 1),
        ),
      );
    }

    return ListView.separated(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 24),
      itemCount: _sessions.length,
      separatorBuilder: (_, __) => const SizedBox(height: 12),
      itemBuilder: (context, i) {
        final s = _sessions[i];
        final arc = _describeArc(s['arc'] as String?);
        final timeSince = _timeSince(s['last_played'] as String?);
        final count = s['session_count'] as int? ?? 1;
        final sig = s['drift_signature'] as String? ?? 'The Drifter';
        final narrator = s['narrator'] as String? ?? '';

        return Container(
          padding: const EdgeInsets.all(18),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.04),
            border: Border.all(color: Colors.white12),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                sig,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 16,
                  fontWeight: FontWeight.w400,
                  letterSpacing: 0.5,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                [narrator, if (arc.isNotEmpty) arc].join(' · '),
                style: const TextStyle(color: Colors.white54, fontSize: 13),
              ),
              const SizedBox(height: 2),
              Text(
                'Drift #$count${timeSince.isNotEmpty ? ' · $timeSince' : ''}',
                style: const TextStyle(color: Colors.white38, fontSize: 11),
              ),
            ],
          ),
        );
      },
    );
  }
}
