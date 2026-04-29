import 'package:flutter/material.dart';
import 'screens/narrator_selection_screen.dart';

void main() {
  runApp(const MythdriftApp());
}

class MythdriftApp extends StatelessWidget {
  const MythdriftApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mythdrift',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.deepPurple,
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      home: const NarratorSelectionScreen(),
    );
  }
}
