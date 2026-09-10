import React from 'react';
import {
  View, Text, StyleSheet, TouchableOpacity,
  FlatList, StatusBar, Image,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, RADIUS, SHADOW } from '../constants/theme';
import { LANGUAGES, useAppStore, Language } from '../store/useAppStore';

export default function LanguageScreen({ navigation }: any) {
  const { selectedLanguage, setLanguage } = useAppStore();

  const handleSelect = (lang: Language) => {
    setLanguage(lang);
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />

      {/* Header */}
      <LinearGradient colors={['#1E1E1E', '#2A2A2A']} style={styles.header}>
        <Text style={styles.brand}>KARIGAR</Text>
        <Text style={styles.tagline}>FROM CRAFT TO MARKET</Text>
        <Text style={styles.heroText}>Your Craft, Your Market{'\n'}आपका हुनर, आपका बाज़ार</Text>
      </LinearGradient>

      {/* Language picker */}
      <View style={styles.body}>
        <Text style={styles.sectionLabel}>CHOOSE LANGUAGE — अपनी भाषा चुनें</Text>

        <FlatList
          data={LANGUAGES}
          keyExtractor={(item) => item.code}
          numColumns={2}
          columnWrapperStyle={styles.row}
          renderItem={({ item }) => {
            const selected = item.code === selectedLanguage.code;
            return (
              <TouchableOpacity
                style={[styles.langBtn, selected && styles.langBtnSelected]}
                onPress={() => handleSelect(item)}
                activeOpacity={0.7}
              >
                <Text style={[styles.langNative, selected && styles.langTextSelected]}>
                  {item.native}
                </Text>
                <Text style={[styles.langLabel, selected && styles.langLabelSelected]}>
                  {item.label}
                </Text>
              </TouchableOpacity>
            );
          }}
        />

        {/* Voice help hint */}
        <View style={styles.voiceHint}>
          <View style={styles.micDot} />
          <Text style={styles.voiceHintText}>VOICE HELP — बोलें to get help</Text>
        </View>

        {/* CTA */}
        <TouchableOpacity
          style={styles.nextBtn}
          onPress={() => navigation.navigate('Main')}
          activeOpacity={0.85}
        >
          <LinearGradient
            colors={[COLORS.primary, COLORS.primaryDark]}
            style={styles.nextGradient}
            start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}
          >
            <Text style={styles.nextText}>आगे बढ़ें — Next →</Text>
          </LinearGradient>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container:   { flex: 1, backgroundColor: COLORS.screenBg },
  header:      { paddingTop: 60, paddingBottom: 32, paddingHorizontal: 24, alignItems: 'center' },
  brand:       { fontSize: 32, fontWeight: '900', color: COLORS.primary, letterSpacing: 4 },
  tagline:     { fontSize: 11, color: '#aaa', letterSpacing: 3, marginTop: 2, marginBottom: 20 },
  heroText:    { fontSize: 20, fontWeight: '700', color: COLORS.white, textAlign: 'center', lineHeight: 30 },
  body:        { flex: 1, paddingHorizontal: 20, paddingTop: 24 },
  sectionLabel:{ fontSize: 11, color: COLORS.textMuted, letterSpacing: 1.5, marginBottom: 16, textAlign: 'center' },
  row:         { justifyContent: 'space-between', marginBottom: 12 },
  langBtn:     {
    flex: 1, marginHorizontal: 4, paddingVertical: 14, paddingHorizontal: 10,
    backgroundColor: COLORS.white, borderRadius: RADIUS.md,
    alignItems: 'center', borderWidth: 2, borderColor: COLORS.border,
    ...SHADOW.sm,
  },
  langBtnSelected: { borderColor: COLORS.primary, backgroundColor: '#FFF3EE' },
  langNative:  { fontSize: 18, fontWeight: '700', color: COLORS.text },
  langLabel:   { fontSize: 12, color: COLORS.textMuted, marginTop: 2 },
  langTextSelected:  { color: COLORS.primary },
  langLabelSelected: { color: COLORS.primary },
  voiceHint:   { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', marginTop: 20, marginBottom: 8 },
  micDot:      { width: 10, height: 10, borderRadius: 5, backgroundColor: COLORS.primary, marginRight: 8 },
  voiceHintText: { fontSize: 13, color: COLORS.textMuted },
  nextBtn:     { marginTop: 16, borderRadius: RADIUS.full, overflow: 'hidden' },
  nextGradient:{ paddingVertical: 16, alignItems: 'center' },
  nextText:    { fontSize: 16, fontWeight: '700', color: COLORS.white },
});
