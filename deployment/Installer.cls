Class App.Installer
{

XData Install [ XMLNamespace = INSTALLER ]
{
<Manifest>
	<Default Name="NAMESPACE" Value="KAFKA"/>
	<Default Name="DBNAME" Value="${NAMESPACE}"/>
	<Default Name="SOURCESPATH" Dir="#{$system.Process.CurrentDirectory()}src/IrisKafkaSink"/>
	<Default Name="RESOURCE" Value="%DB_%DEFAULT"/>

	<Namespace Name="${NAMESPACE}" Code="${DBNAME}" Data="${DBNAME}" Create="yes" Ensemble="1">
		<Configuration>
			<Database Name="${DBNAME}" Dir="${MGRDIR}${DBNAME}" Create="yes" Resource="${RESOURCE}"/>
		</Configuration>

		<Import File="${SOURCESPATH}" Flags="ck" Recurse="1"/>
	</Namespace>
</Manifest>
}

ClassMethod Setup(ByRef pVars, pLogLevel As %Integer = 3, pInstaller As %Installer.Installer, pLogger As %Installer.AbstractLogger) As %Status [ CodeMode = objectgenerator, Internal ]
{
    Return ##class(%Installer.Manifest).%Generate(%compiledclass, %code, "Install")
}

}
