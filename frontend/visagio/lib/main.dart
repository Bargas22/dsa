import 'package:flutter/material.dart';
import 'services/api_service.dart';

const teal = Color(0xFF004F63),
    purple = Color(0xFF7551B5),
    paper = Color(0xFFFFFBF7),
    ink = Color(0xFF183047),
    line = Color(0xFFE4D9EC);
void main() => runApp(const VisagioApp());

class VisagioApp extends StatelessWidget {
  const VisagioApp({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
        debugShowCheckedModeBanner: false,
        title: 'ViSAGiO',
        theme: ThemeData(
          useMaterial3: true,
          fontFamily: 'Roboto',
          scaffoldBackgroundColor: paper,
          colorScheme: ColorScheme.fromSeed(seedColor: teal),
          inputDecorationTheme: const InputDecorationTheme(
            filled: true,
            fillColor: Colors.white,
            border: OutlineInputBorder(
              borderRadius: BorderRadius.all(Radius.circular(12)),
              borderSide: BorderSide(color: line),
            ),
          ),
        ),
        home: const Onboarding(),
      );
}

void open(BuildContext c, Widget page) =>
    Navigator.push(c, MaterialPageRoute(builder: (_) => page));

class PrimaryButton extends StatelessWidget {
  const PrimaryButton(this.text, this.tap, {super.key});
  final String text;
  final VoidCallback tap;
  @override
  Widget build(BuildContext c) => SizedBox(
      width: double.infinity,
      height: 52,
      child: FilledButton(
          onPressed: tap,
          style: FilledButton.styleFrom(
              backgroundColor: teal,
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(28))),
          child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
            Text(text, style: const TextStyle(fontWeight: FontWeight.w700)),
            const SizedBox(width: 24),
            const Icon(Icons.arrow_forward)
          ])));
}

class WaveHeader extends StatelessWidget {
  const WaveHeader(
      {this.title = 'ViSAGiO',
      this.subtitle = 'BELEZA COM PROPÓSITO',
      super.key});
  final String title, subtitle;
  @override
  Widget build(BuildContext c) => Container(
      height: 210,
      width: double.infinity,
      decoration: const BoxDecoration(
          color: teal,
          borderRadius:
              BorderRadius.vertical(bottom: Radius.elliptical(220, 48))),
      child: SafeArea(
          child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
        Text(title,
            style: const TextStyle(
                color: Colors.white,
                fontSize: 38,
                fontWeight: FontWeight.w700,
                letterSpacing: 1)),
        const SizedBox(height: 6),
        Text(subtitle,
            textAlign: TextAlign.center,
            style: const TextStyle(
                color: Colors.white70, fontSize: 11, letterSpacing: 1.8))
      ])));
}

class PageShell extends StatelessWidget {
  const PageShell(
      {required this.title,
      required this.child,
      this.subtitle = '',
      super.key});
  final String title, subtitle;
  final Widget child;
  @override
  Widget build(BuildContext c) => Scaffold(
      appBar: AppBar(
          backgroundColor: teal,
          foregroundColor: Colors.white,
          title: Text(title),
          centerTitle: true),
      body: ListView(padding: const EdgeInsets.all(22), children: [
        if (subtitle.isNotEmpty)
          Text(subtitle,
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.black54)),
        if (subtitle.isNotEmpty) const SizedBox(height: 22),
        child
      ]));
}

class CardTile extends StatelessWidget {
  const CardTile(this.icon, this.title, this.subtitle, {this.tap, super.key});
  final IconData icon;
  final String title, subtitle;
  final VoidCallback? tap;
  @override
  Widget build(BuildContext c) => Card(
      color: Colors.white,
      elevation: 0,
      shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: const BorderSide(color: line)),
      child: ListTile(
          onTap: tap,
          leading: CircleAvatar(
              backgroundColor: const Color(0xFFF1EAF8),
              child: Icon(icon, color: purple)),
          title: Text(title,
              style: const TextStyle(fontWeight: FontWeight.w700, color: ink)),
          subtitle: Text(subtitle),
          trailing: const Icon(Icons.chevron_right, color: purple)));
}

class Onboarding extends StatelessWidget {
  const Onboarding({super.key});
  @override
  Widget build(BuildContext c) => Scaffold(
          body: Column(children: [
        const WaveHeader(),
        const Spacer(),
        Container(
            width: 190,
            height: 190,
            decoration: const BoxDecoration(
                color: Color(0xFFF2ECF7), shape: BoxShape.circle),
            child: const Icon(Icons.face_retouching_natural,
                color: purple, size: 112)),
        const SizedBox(height: 24),
        const Text('Tecnologia e visagismo\npara valorizar sua imagem.',
            textAlign: TextAlign.center,
            style: TextStyle(
                fontSize: 22, fontWeight: FontWeight.w700, color: ink)),
        const Spacer(),
        Padding(
            padding: const EdgeInsets.all(28),
            child: PrimaryButton('Começar agora', () => open(c, const Intro())))
      ]));
}

class Intro extends StatelessWidget {
  const Intro({super.key});
  @override
  Widget build(BuildContext c) => Scaffold(
          body: Column(children: [
        const WaveHeader(
            title: 'Conheça o poder do\nvisagismo com IA',
            subtitle: 'ANALISAMOS SEU ROSTO E RECOMENDAMOS O MELHOR VISUAL'),
        const Spacer(),
        const Icon(Icons.face_unlock_outlined, size: 130, color: purple),
        const SizedBox(height: 24),
        for (final x in [
          ('Análise facial inteligente', Icons.face_retouching_natural),
          ('Recomendações personalizadas', Icons.auto_awesome),
          ('Simulações realistas', Icons.photo_camera_back),
          ('Agende com praticidade', Icons.calendar_month)
        ])
          Padding(
              padding: const EdgeInsets.symmetric(horizontal: 34, vertical: 6),
              child: Row(children: [
                Icon(x.$2, color: purple),
                const SizedBox(width: 14),
                Text(x.$1)
              ])),
        const Spacer(),
        Padding(
            padding: const EdgeInsets.all(28),
            child: PrimaryButton('Próximo', () => open(c, const AuthPage())))
      ]));
}

class AuthPage extends StatefulWidget {
  const AuthPage({super.key});
  @override
  State<AuthPage> createState() => _AuthPageState();
}

class _AuthPageState extends State<AuthPage> {
  bool register = false, loading = false;
  final name = TextEditingController(),
      email = TextEditingController(),
      password = TextEditingController();
  String? error;
  Future<void> submit() async {
    setState(() => loading = true);
    try {
      final data = await ApiService.auth(register ? 'register' : 'login',
          {'name': name.text, 'email': email.text, 'password': password.text});
      if (mounted) {
        Navigator.pushAndRemoveUntil(
            context,
            MaterialPageRoute(
                builder: (_) => Preferences(
                    userName:
                        (data['user']?['name'] ?? 'Bernardo').toString())),
            (_) => false);
      }
    } catch (e) {
      setState(() => error = e.toString());
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext c) => Scaffold(
        body: ListView(children: [
          const WaveHeader(),
          Transform.translate(
            offset: const Offset(0, -24),
            child: Padding(
              padding: const EdgeInsets.all(26),
              child: Column(children: [
                CircleAvatar(
                    radius: 38,
                    backgroundColor: Colors.white,
                    child: Text('V',
                        style: TextStyle(
                            fontSize: 38,
                            color: teal,
                            fontWeight: FontWeight.bold))),
                const SizedBox(height: 12),
                Text(register ? 'Criar conta' : 'Entrar',
                    style: const TextStyle(
                        fontSize: 26, fontWeight: FontWeight.bold, color: ink)),
                const SizedBox(height: 24),
                if (register)
                  TextField(
                      controller: name,
                      decoration: const InputDecoration(
                          labelText: 'Nome completo',
                          prefixIcon: Icon(Icons.person_outline))),
                if (register) const SizedBox(height: 12),
                TextField(
                    controller: email,
                    keyboardType: TextInputType.emailAddress,
                    decoration: const InputDecoration(
                        labelText: 'E-mail',
                        prefixIcon: Icon(Icons.mail_outline))),
                const SizedBox(height: 12),
                TextField(
                    controller: password,
                    obscureText: true,
                    decoration: const InputDecoration(
                        labelText: 'Senha',
                        prefixIcon: Icon(Icons.lock_outline))),
                if (error != null)
                  Padding(
                      padding: const EdgeInsets.all(10),
                      child: Text(error!,
                          style: const TextStyle(color: Colors.red))),
                const SizedBox(height: 18),
                PrimaryButton(
                    loading
                        ? 'Aguarde...'
                        : register
                            ? 'Cadastrar'
                            : 'Entrar',
                    loading ? () {} : submit),
                const SizedBox(height: 12),
                TextButton(
                    onPressed: () => setState(() => register = !register),
                    child: Text(
                        register
                            ? 'Já tem conta? Entrar'
                            : 'Não tem conta? Cadastre-se',
                        style: const TextStyle(color: purple))),
                TextButton.icon(
                  onPressed: () {
                    ApiService.demoMode = true;
                    Navigator.pushAndRemoveUntil(
                        c,
                        MaterialPageRoute(
                            builder: (_) =>
                                const Preferences(userName: 'Visitante')),
                        (_) => false);
                  },
                  icon: const Icon(Icons.visibility_outlined),
                  label: const Text('Entrar no modo de demonstração'),
                ),
              ]),
            ),
          ),
        ]),
      );
}

class Preferences extends StatefulWidget {
  const Preferences({required this.userName, super.key});
  final String userName;
  @override
  State<Preferences> createState() => _PreferencesState();
}

class _PreferencesState extends State<Preferences> {
  int hair = 0, length = 1;
  bool loading = false;

  Future<void> continueToHome() async {
    setState(() => loading = true);
    try {
      await ApiService.savePreferences(
        ['straight', 'wavy', 'curly', 'coily'][hair],
        ['short', 'medium', 'long'][length],
      );
      if (mounted) open(context, Home(userName: widget.userName));
    } catch (error) {
      if (mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text(error.toString())));
      }
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext c) => PageShell(
      title: 'Vamos te conhecer melhor',
      subtitle:
          'Responda algumas perguntas para personalizarmos suas recomendações.',
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Tipo de cabelo',
            style: TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(height: 10),
        Wrap(
            spacing: 8,
            children: List.generate(
                4,
                (i) => ChoiceChip(
                    label: Text(['Liso', 'Ondulado', 'Cacheado', 'Crespo'][i]),
                    selected: hair == i,
                    onSelected: (_) => setState(() => hair = i),
                    selectedColor: const Color(0xFFE5D7F4)))),
        const SizedBox(height: 26),
        const Text('Comprimento do cabelo',
            style: TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(height: 10),
        Wrap(
            spacing: 8,
            children: List.generate(
                3,
                (i) => ChoiceChip(
                    label: Text(['Curto', 'Médio', 'Longo'][i]),
                    selected: length == i,
                    onSelected: (_) => setState(() => length = i),
                    selectedColor: const Color(0xFFE5D7F4)))),
        const SizedBox(height: 34),
        PrimaryButton(loading ? 'Salvando...' : 'Continuar',
            loading ? () {} : continueToHome)
      ]));
}

class Home extends StatelessWidget {
  const Home({required this.userName, super.key});
  final String userName;
  @override
  Widget build(BuildContext c) => Scaffold(
      appBar: AppBar(
          backgroundColor: teal,
          foregroundColor: Colors.white,
          title: Text('Olá, $userName! 👋'),
          actions: [
            IconButton(
                onPressed: () {}, icon: const Icon(Icons.notifications_none))
          ]),
      bottomNavigationBar: NavigationBar(selectedIndex: 0, destinations: const [
        NavigationDestination(icon: Icon(Icons.home_outlined), label: 'Início'),
        NavigationDestination(icon: Icon(Icons.history), label: 'Histórico'),
        NavigationDestination(
            icon: Icon(Icons.add_circle, color: purple), label: 'Analisar'),
        NavigationDestination(
            icon: Icon(Icons.calendar_month), label: 'Agenda'),
        NavigationDestination(icon: Icon(Icons.person_outline), label: 'Perfil')
      ]),
      body: ListView(padding: const EdgeInsets.all(20), children: [
        const Text('Pronto para realçar\nsua melhor versão?',
            style: TextStyle(
                fontSize: 27, fontWeight: FontWeight.bold, color: ink)),
        const SizedBox(height: 22),
        Card(
            color: Colors.white,
            child: ListTile(
                contentPadding: const EdgeInsets.all(18),
                title: const Text('Nova análise',
                    style: TextStyle(fontWeight: FontWeight.bold)),
                subtitle: const Text(
                    'Descubra recomendações personalizadas para você.'),
                trailing: IconButton.filled(
                    onPressed: () => open(c, const CameraGuide()),
                    icon: const Icon(Icons.add),
                    style: IconButton.styleFrom(backgroundColor: purple)))),
        const SizedBox(height: 20),
        const Text('Acesso rápido',
            style: TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        CardTile(Icons.content_cut, 'Cortes', '5 sugestões para você',
            tap: () => open(c, const Recommendations())),
        CardTile(Icons.face, 'Barba', '3 estilos que combinam',
            tap: () => open(c, const BeardColor())),
        CardTile(Icons.palette_outlined, 'Coloração', 'Cores que harmonizam',
            tap: () => open(c, const BeardColor())),
        CardTile(Icons.history, 'Seu histórico', 'Análises e simulações',
            tap: () => open(c, const History())),
        CardTile(Icons.calendar_month, 'Agendamento', 'Escolha um profissional',
            tap: () => open(c, const Booking()))
      ]));
}

class CameraGuide extends StatelessWidget {
  const CameraGuide({super.key});
  @override
  Widget build(BuildContext c) => PageShell(
      title: 'Seu momento de transformação',
      subtitle: 'Prepare-se para uma análise precisa.',
      child: Column(children: [
        const Icon(Icons.face_retouching_natural, size: 150, color: purple),
        for (final x in [
          'Escolha um local bem iluminado',
          'Olhe para frente e mantenha o rosto centralizado',
          'Remova acessórios que cubram o rosto',
          'Use uma expressão neutra'
        ])
          CardTile(Icons.check_circle_outline, x, ''),
        const SizedBox(height: 18),
        PrimaryButton(
            'Iniciar análise', () => open(c, const AnalysisProgress()))
      ]));
}

class AnalysisProgress extends StatefulWidget {
  const AnalysisProgress({super.key});

  @override
  State<AnalysisProgress> createState() => _AnalysisProgressState();
}

class _AnalysisProgressState extends State<AnalysisProgress> {
  bool loading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    runAnalysis();
  }

  Future<void> runAnalysis() async {
    setState(() {
      loading = true;
      error = null;
    });
    try {
      if (ApiService.demoMode) {
        await Future<void>.delayed(const Duration(milliseconds: 800));
      } else {
        final analysis = await ApiService.createAnalysis();
        await ApiService.generateRecommendations(analysis['id'] as int);
      }
    } catch (exception) {
      error = exception.toString();
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext c) => PageShell(
      title: 'Seu formato de rosto',
      subtitle: 'Processando seus traços para criar recomendações.',
      child: Column(children: [
        const SizedBox(height: 30),
        Container(
            width: 220,
            height: 260,
            decoration: BoxDecoration(
                color: const Color(0xFFF1EAF8),
                borderRadius: BorderRadius.circular(110)),
            child: const Icon(Icons.face, size: 150, color: purple)),
        const SizedBox(height: 24),
        Text(
            loading
                ? 'Analisando características...'
                : error == null
                    ? 'Análise concluída e salva na API.'
                    : error!,
            textAlign: TextAlign.center,
            style: TextStyle(
                fontWeight: FontWeight.bold,
                color: error == null ? ink : Colors.red)),
        const SizedBox(height: 12),
        LinearProgressIndicator(value: loading ? .78 : 1, color: purple),
        const SizedBox(height: 8),
        Text(loading ? '78%' : '100%',
            style: const TextStyle(color: purple, fontWeight: FontWeight.bold)),
        const SizedBox(height: 30),
        PrimaryButton(
            loading
                ? 'Aguarde...'
                : error == null
                    ? 'Ver recomendações'
                    : 'Tentar novamente',
            loading
                ? () {}
                : error == null
                    ? () => open(c, const Recommendations())
                    : runAnalysis)
      ]));
}

class Recommendations extends StatefulWidget {
  const Recommendations({super.key});

  @override
  State<Recommendations> createState() => _RecommendationsState();
}

class _RecommendationsState extends State<Recommendations> {
  late Future<List<Map<String, dynamic>>> future;

  @override
  void initState() {
    super.initState();
    future =
        ApiService.demoMode ? Future.value([]) : ApiService.recommendations();
  }

  @override
  Widget build(BuildContext c) => FutureBuilder<List<Map<String, dynamic>>>(
        future: future,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const PageShell(
              title: 'Suas recomendações',
              child: Center(child: CircularProgressIndicator(color: purple)),
            );
          }
          if (snapshot.hasError) {
            return PageShell(
              title: 'Suas recomendações',
              child: Column(children: [
                Text(snapshot.error.toString(), textAlign: TextAlign.center),
                const SizedBox(height: 16),
                PrimaryButton('Tentar novamente', () {
                  setState(() => future = ApiService.recommendations());
                }),
              ]),
            );
          }
          final items = snapshot.data ?? [];
          int count(String category, int fallback) => ApiService.demoMode
              ? fallback
              : items.where((item) => item['category'] == category).length;
          return PageShell(
              title: 'Suas recomendações',
              subtitle:
                  'Selecionamos as melhores opções para realçar sua essência.',
              child: Column(children: [
                CardTile(Icons.content_cut, 'Cortes de cabelo',
                    '${count('haircut', 5)} sugestões para você',
                    tap: () => open(
                        c,
                        Haircuts(
                            initialItems: items
                                .where((item) => item['category'] == 'haircut')
                                .toList()))),
                CardTile(Icons.face, 'Barba',
                    '${count('beard', 3)} estilos que combinam',
                    tap: () => open(c, const BeardColor())),
                CardTile(Icons.palette, 'Coloração',
                    '${count('coloring', 3)} cores que harmonizam',
                    tap: () => open(c, const BeardColor())),
                CardTile(Icons.spa, 'Cuidados',
                    '${count('care', 1)} cuidado recomendado')
              ]));
        },
      );
}

class Haircuts extends StatefulWidget {
  const Haircuts({this.initialItems, super.key});
  final List<Map<String, dynamic>>? initialItems;

  @override
  State<Haircuts> createState() => _HaircutsState();
}

class _HaircutsState extends State<Haircuts> {
  late Future<List<Map<String, dynamic>>> future;

  @override
  void initState() {
    super.initState();
    future = widget.initialItems != null
        ? Future.value(widget.initialItems)
        : ApiService.demoMode
            ? Future.value([])
            : ApiService.recommendations(category: 'haircut');
  }

  List<Map<String, dynamic>> demoItems() => [
        {
          'title': 'Degradê Low Fade',
          'description': 'Moderno e versátil',
          'compatibility': 95
        },
        {
          'title': 'French Crop Texturizado',
          'description': 'Estilo e praticidade',
          'compatibility': 92
        },
        {
          'title': 'Undercut Desconectado',
          'description': 'Ousado e estiloso',
          'compatibility': 89
        },
        {
          'title': 'Taper Fade',
          'description': 'Clássico e elegante',
          'compatibility': 88
        },
        {
          'title': 'Corte Médio Natural',
          'description': 'Leve e sofisticado',
          'compatibility': 86
        },
      ];

  @override
  Widget build(BuildContext c) => FutureBuilder<List<Map<String, dynamic>>>(
      future: future,
      builder: (context, snapshot) {
        final items = ApiService.demoMode ? demoItems() : (snapshot.data ?? []);
        return PageShell(
            title: 'Cortes recomendados',
            subtitle: 'Os cortes que mais combinam com você.',
            child: snapshot.connectionState == ConnectionState.waiting
                ? const Center(child: CircularProgressIndicator(color: purple))
                : snapshot.hasError
                    ? Text(snapshot.error.toString(),
                        textAlign: TextAlign.center)
                    : Column(children: [
                        for (final item in items)
                          CardTile(
                              Icons.content_cut,
                              item['title']?.toString() ?? 'Recomendação',
                              item['description']?.toString() ?? '', tap: () {
                            ApiService.lastRecommendationId =
                                item['id'] as int?;
                            open(
                                c,
                                HaircutDetail(
                                  title: item['title']?.toString() ?? 'Corte',
                                  description: item['description']?.toString(),
                                  compatibility: item['compatibility'] as int?,
                                ));
                          })
                      ]));
      });
}

class HaircutDetail extends StatelessWidget {
  const HaircutDetail(
      {required this.title, this.description, this.compatibility, super.key});
  final String title;
  final String? description;
  final int? compatibility;
  @override
  Widget build(BuildContext c) => PageShell(
      title: title,
      child: Column(children: [
        Container(
            height: 300,
            decoration: BoxDecoration(
                color: teal, borderRadius: BorderRadius.circular(28)),
            child: const Center(
                child: Icon(Icons.person, size: 190, color: Colors.white70))),
        const SizedBox(height: 20),
        Text(
            description ??
                'Um corte moderno e versátil que valoriza o formato do seu rosto e traz equilíbrio.',
            style: TextStyle(fontSize: 16)),
        const SizedBox(height: 16),
        CardTile(Icons.check_circle, 'Compatibilidade',
            '${compatibility ?? 95}% com seus traços'),
        const SizedBox(height: 18),
        PrimaryButton('Simular este corte', () => open(c, const Simulation()))
      ]));
}

class BeardColor extends StatefulWidget {
  const BeardColor({super.key});

  @override
  State<BeardColor> createState() => _BeardColorState();
}

class _BeardColorState extends State<BeardColor> {
  late Future<List<Map<String, dynamic>>> future;

  @override
  void initState() {
    super.initState();
    future =
        ApiService.demoMode ? Future.value([]) : ApiService.recommendations();
  }

  @override
  Widget build(BuildContext c) => FutureBuilder<List<Map<String, dynamic>>>(
      future: future,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const PageShell(
              title: 'Barba e coloração',
              child: Center(child: CircularProgressIndicator(color: purple)));
        }
        final items = snapshot.data ?? [];
        final beards =
            items.where((item) => item['category'] == 'beard').toList();
        final colors =
            items.where((item) => item['category'] == 'coloring').toList();
        return PageShell(
            title: 'Barba e coloração',
            subtitle: 'Recomendações para completar seu visual.',
            child: snapshot.hasError
                ? Text(snapshot.error.toString(), textAlign: TextAlign.center)
                : Column(children: [
                    const Text('Barba',
                        style: TextStyle(
                            fontSize: 18, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 12),
                    if (beards.isEmpty && ApiService.demoMode)
                      const CardTile(Icons.face, 'Barba média desenhada',
                          'Volume controlado e linhas discretas')
                    else
                      for (final item in beards)
                        CardTile(Icons.face, item['title'].toString(),
                            item['description'].toString()),
                    const SizedBox(height: 24),
                    const Text('Coloração',
                        style: TextStyle(
                            fontSize: 18, fontWeight: FontWeight.bold)),
                    if (colors.isEmpty && ApiService.demoMode)
                      const CardTile(Icons.palette, 'Castanho natural',
                          'Harmoniza com seu tom de pele')
                    else
                      for (final item in colors)
                        CardTile(Icons.palette, item['title'].toString(),
                            item['description'].toString()),
                  ]));
      });
}

class Simulation extends StatelessWidget {
  const Simulation({super.key});

  Future<void> save(BuildContext context) async {
    try {
      await ApiService.saveSimulation();
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
            content: Text('Simulação salva pela API no histórico.')));
      }
    } catch (error) {
      if (context.mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text(error.toString())));
      }
    }
  }

  @override
  Widget build(BuildContext c) => PageShell(
        title: 'Simulação',
        subtitle: 'Veja como você fica com seu novo visual.',
        child: Column(children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(28),
            child: Container(
              height: 390,
              color: teal,
              child: Row(children: [
                Expanded(
                    child: Container(
                        color: Colors.black12,
                        child: const Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.person,
                                  size: 150, color: Colors.white70),
                              Text('Antes',
                                  style: TextStyle(color: Colors.white))
                            ]))),
                Expanded(
                    child: Container(
                        color: Colors.white12,
                        child: const Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.face_retouching_natural,
                                  size: 150, color: Colors.white),
                              Text('Depois',
                                  style: TextStyle(color: Colors.white))
                            ]))),
              ]),
            ),
          ),
          const SizedBox(height: 20),
          PrimaryButton('Salvar resultado', () => save(c)),
        ]),
      );
}

class History extends StatefulWidget {
  const History({super.key});

  @override
  State<History> createState() => _HistoryState();
}

class _HistoryState extends State<History> {
  late Future<List<Map<String, dynamic>>> future;

  @override
  void initState() {
    super.initState();
    future = ApiService.demoMode ? Future.value([]) : ApiService.analyses();
  }

  @override
  Widget build(BuildContext c) => FutureBuilder<List<Map<String, dynamic>>>(
      future: future,
      builder: (context, snapshot) {
        final items = snapshot.data ?? [];
        return PageShell(
            title: 'Histórico',
            subtitle: 'Suas análises e simulações.',
            child: snapshot.connectionState == ConnectionState.waiting
                ? const Center(child: CircularProgressIndicator(color: purple))
                : snapshot.hasError
                    ? Text(snapshot.error.toString(),
                        textAlign: TextAlign.center)
                    : Column(children: [
                        if (ApiService.demoMode)
                          for (int i = 4; i > 0; i--)
                            CardTile(Icons.person, 'Análise #$i',
                                '${10 + i}/06/2026',
                                tap: () => open(c, const Recommendations()))
                        else if (items.isEmpty)
                          const Padding(
                            padding: EdgeInsets.all(24),
                            child: Text('Nenhuma análise realizada ainda.'),
                          )
                        else
                          for (final item in items)
                            CardTile(
                                Icons.person,
                                'Análise #${item['id']}',
                                item['created_at']
                                        ?.toString()
                                        .split('T')
                                        .first ??
                                    '', tap: () {
                              ApiService.lastAnalysisId = item['id'] as int?;
                              open(c, const Recommendations());
                            }),
                        const SizedBox(height: 20),
                        PrimaryButton(
                            'Nova análise', () => open(c, const CameraGuide()))
                      ]));
      });
}

class Booking extends StatefulWidget {
  const Booking({super.key});
  @override
  State<Booking> createState() => _BookingState();
}

class _BookingState extends State<Booking> {
  int professional = 0, day = 2, time = 1;
  bool saving = false;
  late Future<List<Map<String, dynamic>>> future;

  static const availableTimes = [
    '08:00',
    '10:00',
    '11:00',
    '13:00',
    '14:00',
    '16:00'
  ];

  @override
  void initState() {
    super.initState();
    future = ApiService.demoMode
        ? Future.value([
            {
              'id': 1,
              'name': 'Studio Alpha',
              'specialty': 'Barbearia premium',
              'rating': 4.9
            },
            {
              'id': 2,
              'name': 'Leandro Silva',
              'specialty': 'Especialista',
              'rating': 4.8
            },
            {
              'id': 3,
              'name': 'Beleza & Estilo',
              'specialty': 'Salão de beleza',
              'rating': 4.7
            },
          ])
        : ApiService.professionals();
  }

  Future<void> confirm(List<Map<String, dynamic>> professionals) async {
    if (professionals.isEmpty) return;
    setState(() => saving = true);
    try {
      if (!ApiService.demoMode) {
        final selectedDay = DateTime.now().add(Duration(days: day + 1));
        final parts = availableTimes[time].split(':');
        final appointmentDate = DateTime(
          selectedDay.year,
          selectedDay.month,
          selectedDay.day,
          int.parse(parts[0]),
          int.parse(parts[1]),
        );
        await ApiService.createAppointment(
          professionalId: professionals[professional]['id'] as int,
          appointmentDate: appointmentDate,
        );
      }
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
            content: Text('Agendamento confirmado e salvo pela API!')));
      }
    } catch (error) {
      if (mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text(error.toString())));
      }
    } finally {
      if (mounted) setState(() => saving = false);
    }
  }

  @override
  Widget build(BuildContext c) => FutureBuilder<List<Map<String, dynamic>>>(
      future: future,
      builder: (context, snapshot) {
        final professionals = snapshot.data ?? [];
        final dates = List.generate(
            6, (index) => DateTime.now().add(Duration(days: index + 1)));
        return PageShell(
            title: 'Agendamento',
            subtitle: 'Escolha um profissional.',
            child: snapshot.connectionState == ConnectionState.waiting
                ? const Center(child: CircularProgressIndicator(color: purple))
                : snapshot.hasError
                    ? Text(snapshot.error.toString(),
                        textAlign: TextAlign.center)
                    : Column(children: [
                        for (int i = 0; i < professionals.length; i++)
                          Card(
                              child: ListTile(
                                  onTap: () => setState(() => professional = i),
                                  leading: Icon(
                                      professional == i
                                          ? Icons.radio_button_checked
                                          : Icons.radio_button_off,
                                      color: purple),
                                  title:
                                      Text(professionals[i]['name'].toString()),
                                  subtitle: Text(
                                      '${professionals[i]['specialty'] ?? ''} · ★ ${professionals[i]['rating'] ?? ''}'))),
                        const SizedBox(height: 16),
                        const Text('Selecione a data',
                            style: TextStyle(fontWeight: FontWeight.bold)),
                        Wrap(
                            spacing: 8,
                            children: List.generate(
                                dates.length,
                                (i) => ChoiceChip(
                                    label: Text('${dates[i].day}'),
                                    selected: day == i,
                                    onSelected: (_) =>
                                        setState(() => day = i)))),
                        const SizedBox(height: 18),
                        const Text('Horários disponíveis',
                            style: TextStyle(fontWeight: FontWeight.bold)),
                        Wrap(
                            spacing: 8,
                            children: List.generate(
                                availableTimes.length,
                                (i) => ChoiceChip(
                                    label: Text(availableTimes[i]),
                                    selected: time == i,
                                    onSelected: (_) =>
                                        setState(() => time = i)))),
                        const SizedBox(height: 28),
                        PrimaryButton(
                            saving ? 'Confirmando...' : 'Confirmar agendamento',
                            saving ? () {} : () => confirm(professionals))
                      ]));
      });
}
