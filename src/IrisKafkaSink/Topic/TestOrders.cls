/// Example subclass for the "orders" topic.
/// Demonstrates the pattern of adding computed properties to expose
/// specific payload fields as indexed SQL columns while keeping the
/// full document in the Payload property.
Class IrisKafkaSink.Topic.TestOrders Extends IrisKafkaSink.Core.Message [ ClassType = persistent ]
{

/// Order ID extracted from payload — useful for direct lookups
/// by business key. Calculated on the fly, indexed for fast access.
Property OrderId As %String(MAXLEN = 64) [ SqlComputed, SqlComputeCode = {Set {*} = ..GetByPath({Payload}, "order_id")}, SqlComputeOnChange = %%INSERT ];
 
/// Order total amount — useful for analytical aggregations
Property Amount As %Numeric(SCALE = 2) [ SqlComputed, SqlComputeCode = {Set {*} = ..GetByPath({Payload}, "amount")}, SqlComputeOnChange = %%INSERT ];
 
/// Customer name from nested object: payload.customer.name
/// Demonstrates how to access nested JSON fields via chained %Get calls.
Property CustomerName As %String(MAXLEN = 255) [ SqlComputed, SqlComputeCode = {Set {*} = ..GetByPath({Payload}, "customer.name")}, SqlComputeOnChange = %%INSERT ];
 
/// Standard index for unique-ish values like order IDs
Index OrderIdIdx On OrderId;
 
/// Bitmap index works best for low-cardinality fields
/// (e.g. limited set of customer names, statuses, categories).
/// For high-cardinality fields prefer the standard index type.
Index CustomerIdx On CustomerName [ Type = bitmap ];

Storage Default
{
<Data name="Payload">
<Attribute>Payload</Attribute>
<Structure>node</Structure>
<Subscript>"Payload"</Subscript>
</Data>
<Data name="TestOrdersDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>OrderId</Value>
</Value>
<Value name="3">
<Value>Amount</Value>
</Value>
<Value name="4">
<Value>CustomerName</Value>
</Value>
<Value name="5">
<Value>MessageKey</Value>
</Value>
<Value name="6">
<Value>KafkaTimestamp</Value>
</Value>
<Value name="7">
<Value>CreatedAt</Value>
</Value>
<Value name="8">
<Value>SchemaId</Value>
</Value>
<Value name="9">
<Value>ProtoType</Value>
</Value>
<Value name="10">
<Value>KafkaOffset</Value>
</Value>
<Value name="11">
<Value>Partition</Value>
</Value>
<Value name="12">
<Value>Topic</Value>
</Value>
</Data>
<DataLocation>^IrisKafkaSink.T74BF.TestOrdersD</DataLocation>
<DefaultData>TestOrdersDefaultData</DefaultData>
<IdLocation>^IrisKafkaSink.T74BF.TestOrdersD</IdLocation>
<IndexLocation>^IrisKafkaSink.T74BF.TestOrdersI</IndexLocation>
<StreamLocation>^IrisKafkaSink.T74BF.TestOrdersS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
