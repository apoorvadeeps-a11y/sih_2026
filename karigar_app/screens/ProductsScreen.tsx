import React, { useEffect, useState } from 'react';
import {
  View, Text, StyleSheet, FlatList,
  TouchableOpacity, ActivityIndicator, RefreshControl,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, RADIUS, SHADOW } from '../constants/theme';
import { useAppStore, Product } from '../store/useAppStore';
import { listProducts } from '../services/api';

export default function ProductsScreen({ navigation }: any) {
  const { products, setProducts } = useAppStore();
  const [loading, setLoading]     = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  const load = async (silent = false) => {
    if (!silent) setLoading(true);
    try {
      const r = await listProducts();
      setProducts(r.products);
    } catch { /* use cached */ } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => { load(); }, []);

  const renderItem = ({ item }: { item: Product }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => navigation.navigate('ProductDetail', { product: item })}
      activeOpacity={0.75}
    >
      <View style={styles.cardLeft}>
        <View style={styles.iconBox}>
          <Ionicons name="cube-outline" size={26} color={COLORS.primary} />
        </View>
        <View style={{ flex: 1 }}>
          <Text style={styles.title} numberOfLines={1}>{item.title}</Text>
          {item.title_hi && (
            <Text style={styles.titleHi} numberOfLines={1}>{item.title_hi}</Text>
          )}
          <Text style={styles.meta}>{item.category} · {item.craft_technique}</Text>
        </View>
      </View>
      <View style={styles.priceBox}>
        <Text style={styles.price}>₹{item.suggested_price}</Text>
        <Text style={styles.sku}>{item.sku}</Text>
      </View>
    </TouchableOpacity>
  );

  if (loading && products.length === 0) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={COLORS.primary} />
        <Text style={styles.loadingText}>Loading products...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>My Products — मेरी चीज़ें</Text>
        <Text style={styles.headerCount}>{products.length} total</Text>
      </View>

      <FlatList
        data={products}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={styles.list}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={() => { setRefreshing(true); load(true); }}
            tintColor={COLORS.primary}
          />
        }
        ListEmptyComponent={
          <View style={styles.empty}>
            <Ionicons name="cube-outline" size={52} color={COLORS.border} />
            <Text style={styles.emptyTitle}>No products yet</Text>
            <Text style={styles.emptySubtitle}>Record your first product to get started</Text>
            <TouchableOpacity
              style={styles.addBtn}
              onPress={() => navigation.navigate('Record')}
            >
              <Text style={styles.addBtnText}>+ Add Product</Text>
            </TouchableOpacity>
          </View>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container:    { flex: 1, backgroundColor: COLORS.screenBg },
  center:       { flex: 1, alignItems: 'center', justifyContent: 'center' },
  loadingText:  { marginTop: 12, color: COLORS.textMuted },
  header:       { padding: 20, paddingBottom: 10, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  headerTitle:  { fontSize: 18, fontWeight: '800', color: COLORS.text },
  headerCount:  { fontSize: 13, color: COLORS.textMuted },
  list:         { padding: 16, paddingTop: 4 },
  card:         { backgroundColor: COLORS.white, borderRadius: RADIUS.lg, padding: 14, marginBottom: 10, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', ...SHADOW.sm },
  cardLeft:     { flexDirection: 'row', alignItems: 'center', flex: 1 },
  iconBox:      { width: 44, height: 44, borderRadius: 22, backgroundColor: '#FFF3EE', alignItems: 'center', justifyContent: 'center', marginRight: 12 },
  title:        { fontSize: 15, fontWeight: '700', color: COLORS.text },
  titleHi:      { fontSize: 13, color: COLORS.textMuted, marginTop: 1 },
  meta:         { fontSize: 12, color: COLORS.textMuted, marginTop: 2 },
  priceBox:     { alignItems: 'flex-end' },
  price:        { fontSize: 16, fontWeight: '800', color: COLORS.primary },
  sku:          { fontSize: 10, color: COLORS.textMuted, marginTop: 2 },
  empty:        { alignItems: 'center', paddingTop: 80 },
  emptyTitle:   { fontSize: 18, fontWeight: '700', color: COLORS.text, marginTop: 16 },
  emptySubtitle:{ fontSize: 14, color: COLORS.textMuted, marginTop: 6, textAlign: 'center' },
  addBtn:       { marginTop: 24, backgroundColor: COLORS.primary, paddingHorizontal: 28, paddingVertical: 14, borderRadius: RADIUS.full },
  addBtnText:   { color: COLORS.white, fontWeight: '700', fontSize: 15 },
});
