	<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="text" indent="no"/>
	<xsl:strip-space elements="*"/>

	<!--Dans le document suivant, la variable r correspond à une liste 
		qui sera affectée avec des valeurs possibles des paramètres d'une requête HTTP.
		Ceux-ci peuvent être valides ou bien fuzzés (i.e fuzzés ou frelatés).

		La variable liste_tuples correspond au résultat de l'analyse des arguments
		passés lors de l'appel à la fonction principale request_generator(). Cette dernière génère
		1 paramètre de chaque type de paramètre d'une requête HTTP (valides ou invalides)-->

	<!--Template pour insérer un retour à la ligne dans le fichier généré-->
	<xsl:template name="newline">
		<xsl:text>&#10;</xsl:text>
	</xsl:template>

	<xsl:template name="indentation">
		<xsl:param name="depth"/>
		<xsl:if test="$depth > 0">
			<xsl:text>	</xsl:text>
			<xsl:call-template name="indentation">
				<xsl:with-param name="depth">
					<xsl:value-of select="$depth - 1"></xsl:value-of>
				</xsl:with-param>
			</xsl:call-template>
		</xsl:if>
	</xsl:template>

	<!--Template pour générer la fonction preambule-->
	<xsl:template match="preambule">
		<xsl:apply-templates select="defaultlibraries" />
		<xsl:apply-templates select="library" />
		<xsl:text>def preambule():</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:apply-templates select="extcall">
			<xsl:with-param name="depth" select="1"/>
		</xsl:apply-templates>
	</xsl:template>

	<!--Template pour générer la fonction preambule-->
	<xsl:template match="postambule">
		<xsl:text>def postambule():</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:text>	pass</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:apply-templates select="extcall">
			<xsl:with-param name="depth" select="1"/>
		</xsl:apply-templates>
		<xsl:call-template name="params_availabled" />
		<xsl:text>if __name__ == "__main__":</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:text>	main(sys.argv[1:])</xsl:text>
		<xsl:call-template name="newline"/>
	</xsl:template>

        <xsl:template name="params_availabled">
                <xsl:text>def params_availabled():</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:text>	r = []</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:for-each select="//generatorAffectation">
			<xsl:text>	r.append("</xsl:text>
      			<xsl:value-of select="@id"/>
			<xsl:variable name="search_name" select="@name" />
			<xsl:if test="//parameters[@name=$search_name]/@type = 'unsuitable'">
				<xsl:text>.*</xsl:text>
			</xsl:if>    			
    			<xsl:text>")</xsl:text>
			<xsl:call-template name="newline"/>
    		</xsl:for-each>
		<xsl:text>	return r</xsl:text>
		<xsl:call-template name="newline"/>
        </xsl:template>

	<!--Template insérant les librairie python nécessaires au fichier généré
		Le path système est modifier afin de pouvoir importer des modules propres au projet Schnapi-->
	<xsl:template match="defaultlibraries">
		<xsl:param name="depth"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>import sys</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:text>sys.path.append('./fuzzerlib/')</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:text>import string</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:text>import random</xsl:text>
		<xsl:call-template name="newline"/>
	</xsl:template>

	<!--Template insérant les modules du projet (ex : fuzzerlib pour la génération aléatoire)-->
	<xsl:template match="library">
		<xsl:param name="depth"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>from </xsl:text><xsl:value-of select="normalize-space(@name)"/><xsl:text> import *</xsl:text>
		<xsl:call-template name="newline"/>
	</xsl:template>

	<!--Template permettant d'appeler une fonction avec ses arguments-->
	<xsl:template match="extcall">
		<xsl:param name="depth"/>
		<xsl:param name="parameter"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:value-of select="normalize-space(@name)"/>
		<xsl:text>(</xsl:text>
		<xsl:value-of select="normalize-space(@parameter)"/>
		<xsl:text>)</xsl:text>
		<xsl:call-template name="newline"/>
	</xsl:template>

	<!--Template permettant d'effectuer une affectation à la variable r moyennant
		l'appel à la fonction string_generator du module fuzzerlib-->
	<xsl:template match="string">
		<xsl:param name="depth"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>r += [string_generator(</xsl:text>
		<xsl:value-of select="normalize-space(@lenmin)"/>
		<xsl:text>, </xsl:text>
		<xsl:value-of select="normalize-space(@lenmax)"/>
		<xsl:text>, </xsl:text>
		<xsl:value-of select="normalize-space(@chars)"/>
		<xsl:text>)]</xsl:text>
		<xsl:call-template name="newline"/>
	</xsl:template>

	<!--Template permettant d'affecter une certaine valeur passsée en attribut de la balise xml matchée
		à la variable r-->
	<xsl:template match="value">
		<xsl:param name="depth"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>r += [</xsl:text>
		<xsl:value-of select="normalize-space(@value)"/>
		<xsl:text>]</xsl:text>
		<xsl:call-template name="newline"/>
	</xsl:template>

	<!--Template permettant d'effectuer une affectation à la variable r moyennant l'appel à une fonction qui sera générée-->
	<xsl:template match="call">
		<xsl:param name="depth"/>
		<xsl:param name="parameter"/> 
		<xsl:call-template name="indentation">
			<xsl:with-param name="depth" select="$depth"/>
		</xsl:call-template>
		<xsl:text>r += [</xsl:text>
		<xsl:value-of select="normalize-space(@name)"/>
		<xsl:text>(</xsl:text>
		<xsl:value-of select="normalize-space(@parameter)"/>
		<xsl:text>)]</xsl:text>
		<xsl:call-template name="newline"/>
	</xsl:template>

	<!--Même template que le précédent à la différence qu'il appelle une fonction 
		avec un paramètre précis qui ne doit pas être précisé dans la description xml 
		car il ne dépend que du choix de l'implémentation de la tranformation-->
	<xsl:template match="generatorAffectation">
		<xsl:param name="depth"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>r += [</xsl:text>
		<xsl:value-of select="normalize-space(@name)"/>
		<xsl:text>(tuple_list, is_fuzz_requested(tuple_list, "</xsl:text>
		<xsl:value-of select="normalize-space(@id)"/>
		<xsl:text>"))]</xsl:text>
		<xsl:call-template name="newline"/>
	</xsl:template>

	<!--Template permettant de créer la fonction main et d'appeler la fonction 
		de génération des paramètres de fuzzing-->
	<xsl:template match="main">
		<xsl:text>def main(args):</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:text>	r = </xsl:text>
		<xsl:value-of select="normalize-space(@generator)"/>
		<xsl:text>(args)</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:apply-templates select="extcall">
			<xsl:with-param name="depth">
				<xsl:value-of select="1"></xsl:value-of>
			</xsl:with-param>
		</xsl:apply-templates>
	</xsl:template>

	<!--Template créant la fonction principale de génération de paramètre pour une requêtre HTTP
		La liste de ces paramètre est renvoyée dans la variable r-->
	<xsl:template match="generator">
		<xsl:text>def </xsl:text>
		<xsl:value-of select="normalize-space(@name)"/>
		<xsl:text>(args):</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:text>	r = []</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:text>	tuple_list = args</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:apply-templates select="*">
			<xsl:with-param name="depth">
				<xsl:value-of select="1"></xsl:value-of>
			</xsl:with-param>
		</xsl:apply-templates>
		<xsl:text>	return r</xsl:text>
		<xsl:call-template name="newline"/>
	</xsl:template>

	<!--Template créant une fonction à partir de la description d'un paramètre
		(grace à son type et une énumération de valeur valides (i.e reconnues par le protocole)-->
	<xsl:template match="parameters">
		<xsl:param name="depth"/>
		<xsl:text>def </xsl:text>
		<xsl:value-of select="normalize-space(@name)"/>
		<xsl:text>(</xsl:text>
		<xsl:text>tuple_list, fuzz</xsl:text>
		<xsl:text>):</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:text>	context = []</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:text>	r = []</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:text>	l = None</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:text>	d = None</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:text>	i = None</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:choose>
			<xsl:when test="not(normalize-space(@type) = 'unsuitable')">
				<xsl:text>	if fuzz:</xsl:text>
				<xsl:call-template name="newline"/>
				<xsl:text>		r += [[abnfgen_</xsl:text>
				<xsl:value-of select="normalize-space(@type)"/>
				<xsl:text>()]]</xsl:text>
				<xsl:call-template name="newline"/>
				<xsl:text>	else : </xsl:text>
				<xsl:call-template name="newline"/>
				<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth + 2"/></xsl:call-template>
				<xsl:apply-templates select="*">
					<xsl:with-param name="depth">
						<xsl:value-of select="2"></xsl:value-of>
					</xsl:with-param>
				</xsl:apply-templates>
				<xsl:call-template name="newline"/>
			</xsl:when>
			<xsl:otherwise><xsl:apply-templates select="*">
				<xsl:with-param name="depth"><xsl:value-of select="1"></xsl:value-of></xsl:with-param></xsl:apply-templates>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:text>	return r</xsl:text>
		<xsl:call-template name="newline"/>
	</xsl:template>

	<!--Template permettant d'effectuer une boucle for-->
	<xsl:template match="loop">
		<xsl:param name="depth"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>context.append(i)</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>for i in range(</xsl:text>
		<xsl:value-of select="normalize-space(@itermin)"/>
		<xsl:text>, </xsl:text>
		<xsl:value-of select="normalize-space(@itermax)"/>
		<xsl:text> + 1):</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:apply-templates select="*">
			<xsl:with-param name="depth">
				<xsl:value-of select="$depth + 1"></xsl:value-of>
			</xsl:with-param>
		</xsl:apply-templates>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>i = context.pop()</xsl:text>
		<xsl:call-template name="newline"/>
	</xsl:template>

	<!--Template permetant de traiter la liste de valeurs appelée r afin de n'en choisir qu'une seule
		grace à un appelle à la fonction randint du module random.
		L'attribut @number du choice permet d'indiquer le nombre de valeurs à récupérer dans r.
		NB : Gestion des listes et des dictionnaires-->
	<xsl:template match="choice">
		<xsl:param name="depth"/>
		<!-- Vérifie que le noeud fils fasse parti de la liste autorisée -->
		<xsl:if test="not(./list | ./dictionary)">
		    <xsl:message terminate="no">Node error between list node</xsl:message>
		</xsl:if>
		<xsl:apply-templates select="./*">
			<xsl:with-param name="depth">
				<xsl:value-of select="$depth"></xsl:value-of>
			</xsl:with-param>
		</xsl:apply-templates>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:choose>
		  <xsl:when test="./list">
			<xsl:text>l = r[len(r)-1]</xsl:text>
			<xsl:call-template name="newline"/>
			<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
			<xsl:text>r[len(r)-1] = []</xsl:text>
			<xsl:call-template name="newline"/>
			<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		  </xsl:when>
		  <xsl:when test="./dictionary">
		    <xsl:text>d = r[len(r)-1]</xsl:text>
			<xsl:call-template name="newline"/>
			<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
			<xsl:text>r[len(r)-1] = []</xsl:text>
			<xsl:call-template name="newline"/>
			<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
			<xsl:text>l = list(d.keys())</xsl:text>
			<xsl:call-template name="newline"/>
			<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		  </xsl:when>
		</xsl:choose>
		<xsl:text>element_done = []</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>for i in range(</xsl:text>
		<xsl:choose>
		  <xsl:when test="@number = '*'">
		    <xsl:text>random.randint(0, len(l)-1)</xsl:text>
		  </xsl:when>
		  <xsl:when test="@number = '+'">
		    <xsl:text>random.randint(1, len(l)-1)</xsl:text>
		  </xsl:when>
		  <xsl:otherwise>
			<xsl:value-of select="normalize-space(@number)"/>
		  </xsl:otherwise>
		</xsl:choose>
		<xsl:text>) :</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth + 1"/></xsl:call-template>
		<xsl:text>e = random.choice(l)</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth + 1"/></xsl:call-template>
		<xsl:text>while (e in element_done): </xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth + 2"/></xsl:call-template>
		<xsl:text>e = random.choice(l)</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth + 1"/></xsl:call-template>
		<xsl:choose>
		  <xsl:when test="./list">
			<xsl:text>r[len(r)-1] += [e</xsl:text>
			<xsl:if test="@number != 1 and @separator != ''">
				<xsl:text> + "</xsl:text>
				<xsl:value-of select="normalize-space(@separator)"/>
				<xsl:text>"</xsl:text>
			</xsl:if>
			<xsl:text>]</xsl:text>
		  </xsl:when>
		  <xsl:when test="./dictionary">
		  	<xsl:text>r[len(r)-1] += [str(e)+":"+str(d.pop(e))</xsl:text>
			<xsl:if test="@number != 1 and @separator != ''">
				<xsl:text> + "</xsl:text>
                                <xsl:value-of select="normalize-space(@separator)"/>
                                <xsl:text>"</xsl:text>
			</xsl:if>
			<xsl:text>]</xsl:text>
		  </xsl:when>
		</xsl:choose>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth + 1"/></xsl:call-template>	
		<xsl:text>element_done.append(e)</xsl:text>
		<xsl:call-template name="newline"/>
		<!--<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>	
		<xsl:text>r = transform_to_final_form(r)</xsl:text>
		<xsl:call-template name="newline"/>-->
	</xsl:template>

	<!--Template permettant de gérerer le code python associé à la définition 
		de valeurs valides de paramètres sont données sous forme de listes.
		On retrouve ici une gestion des contextes-->
	<xsl:template match="list">
		<xsl:param name="depth"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>context.append(l)</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>l = []</xsl:text>
		<xsl:call-template name="newline"/>	
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>	
		<xsl:text>context.append(r)</xsl:text>	
		<xsl:call-template name="newline"/>	
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>	
		<xsl:text>r = []</xsl:text>	
		<xsl:call-template name="newline"/>	
		<xsl:apply-templates select="./*">	
			<xsl:with-param name="depth">	
				<xsl:value-of select="$depth"/>	
			</xsl:with-param>	
		</xsl:apply-templates>	
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>	
		<xsl:text>l = r</xsl:text>	
		<xsl:call-template name="newline"/>	
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>	
		<xsl:text>r = context.pop()</xsl:text>	
		<xsl:call-template name="newline"/>	
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>	
		<xsl:text>r += [l]</xsl:text>	
		<xsl:call-template name="newline"/>	
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>	
		<xsl:text>l = context.pop()</xsl:text>
	</xsl:template>

	<!--Template duale du précédent gérant la création d'un dictionnaire -->
	<xsl:template match="dictionary">
		<xsl:param name="depth"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>context.append(d)</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>d = {}</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:apply-templates select="./*">
			<xsl:with-param name="depth">
				<xsl:value-of select="$depth"/>
			</xsl:with-param>
		</xsl:apply-templates>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>r += [d]</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>d = context.pop()</xsl:text>
		<xsl:call-template name="newline"/>
	</xsl:template>

	<!--Ce template sera toujours appelé dans le template précédent car il gère la création des couples composants un dictionnaire : couple = (clé, valeur)-->
	<xsl:template match="couple">
		<xsl:param name="depth"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>context.append(r)</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>r = []</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:apply-templates select="./key/*">
			<xsl:with-param name="depth">
				<xsl:value-of select="$depth"/>
			</xsl:with-param>
		</xsl:apply-templates>
		<xsl:apply-templates select="./value/*">
			<xsl:with-param name="depth">
				<xsl:value-of select="$depth"/>
			</xsl:with-param>
		</xsl:apply-templates>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>if len(r[1]) == 0:</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth + 1"/></xsl:call-template>
		<xsl:text>d[r[0]] = r[1]</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>else:</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth + 1"/></xsl:call-template>
		<xsl:text>d[r[0]] = r[1][0][0]</xsl:text>
		<xsl:call-template name="newline"/>
		<xsl:call-template name="indentation"><xsl:with-param name="depth" select="$depth"/></xsl:call-template>
		<xsl:text>r = context.pop()</xsl:text>
		<xsl:call-template name="newline"/>
	</xsl:template>

</xsl:stylesheet>
