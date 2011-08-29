Любая страница состоит из вложенных блоков (div, p, span, ...). Как правило,
для их содержимого неважно, внутрь какого родителя они вложены, важно только их
содержимое. Тем не менее, соображения вёрстки и разметки всей страницы приводят
к тому, что иерархия контейнеров довольно жёстко фиксируется в коде, что 
затрудняет его первоначальное освоение, поддержку и модификацию.

Цель данного проекта - обкатать идею движка, где каждый контейнер знает только
своего родителя, сам создаёт своих потомков, и имеет несколько представлений 
самого себя (html, editor, ...). С помощью AJAX мы можем выбирать представление, 
работая с изолированным блоком прямо из тела страницы.

Ориентировочно это позволит создать набор элементов, из которых, как из 
конструктора, можно сделать сайт произвольной структуры наподобие того, как из
элементов gtk собирается интерфейс.