#encoding "utf-8"
#GRAMMAR_ROOT S

Actions -> Word<kwtype=actions_on_law>;
Parts -> Noun<kwtype=parts_of_law>;

Nums -> AnyWord<wff="[1-9]+">;

Article -> Parts<gc-agr[1]>  Adj<gram='ANUM', gc-agr[1]>;
Article -> Parts Nums;
Article_end -> 'после' 'слово'<gram='pl, gen'>;
Articles -> Article+ (Article_end);

Break -> AnyWord<wff=";"> | EOSent;
Amend_part -> AnyWord+ AnyWord;
Law -> AnyWord<h-reg1> AnyWord+;

Quote -> QuoteDbl | QuoteSng | AnyWord<wff="«"> | AnyWord<wff="»">;

Amend -> Quote Amend_part interp (Amendment.Amend::not_norm) Quote;
AmendChng -> Quote Amend_part interp (Amendment.AmendChng::not_norm) Quote;

Content -> 'следующий' 'содержание' Colon;
WordContent -> 'слово' Content;
Indent -> 'абзац' Nums;

Article_spec -> 'статья' '303';

//general
S -> 'внести' 'в' Law interp (Amendment.Law::not_norm) LBracket;
S -> 'внести' 'в' Article_spec interp (Amendment.Article) Law interp (Amendment.Law::not_norm) LBracket;
//S -> 'внести' 'в' Article interp (Amendment.Article) Law interp (Amendment.Law::not_norm) LBracket AnyWord+ RBracket 'следующий' 'изменение' Colon Nums RBracket 'в' Article<gram='gen'> interp (+Amendment.Article) Changes; 

S -> 'в' Articles interp (Amendment.Article) Amend Actions interp (Amendment.Action::not_norm) WordContent AmendChng;
S -> 'в' Articles interp (Amendment.Article) Actions interp (Amendment.Action::not_norm) Indent interp (Amendment.Amend::not_norm) Content AmendChng AnyWord+ interp (+Amendment.AmendChng::not_norm) Break;


//change
Change -> 'слово' Amend Actions interp (Amendment.Action::not_norm) 'слово'<gram='ins'> AmendChng (Comma); 
Changes -> Change* Change Break;
S -> 'в' Article<gram='gen'> interp (Amendment.Article) Changes (Say); 

//say
Type -> 'в' 'следующий' 'редакция' Colon;
Say -> Articles interp (Amendment.Article) Actions interp (Amendment.Action::not_norm) Type Amend;
S -> Say;

//Exclude type
S -> Articles<gram='~nom'> interp (Amendment.Article) Law interp (Amendment.Law::not_norm) LBracket;
S -> 'слово'<gram="pl"> Amend Actions interp (Amendment.Action::not_norm);

