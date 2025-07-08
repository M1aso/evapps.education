export type Locale = 'en' | 'ru'

const dictionaries = {
  en: () => import('../dictionaries/en.json').then((m) => m.default),
  ru: () => import('../dictionaries/ru.json').then((m) => m.default),
}

export const getDictionary = async (locale: Locale) => dictionaries[locale]()
