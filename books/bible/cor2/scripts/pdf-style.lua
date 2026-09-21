function Span(el)
  if el.classes:includes('scripture-gold') then
    local result = pandoc.List({pandoc.RawInline('latex', '\\textcolor{ScriptureGold}{')})
    result:extend(el.content)
    result:insert(pandoc.RawInline('latex', '}'))
    return result
  end
end
