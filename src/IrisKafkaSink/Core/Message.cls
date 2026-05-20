/// Base class for all Kafka sink target tables.
/// Each topic should have its own subclass that may add computed properties
/// and indexes for frequently queried payload fields.
///
/// Storage strategy: full protobuf message is converted to JSON and stored
/// as a single %DynamicObject. Kafka metadata is stored as flat properties
/// for fast filtering and deduplication.
Class IrisKafkaSink.Core.Message Extends %Persistent [ Abstract, ClassType = "" ]
{
 
/// Source topic name
Property Topic As %String(MAXLEN = 255) [ Required ];
 
/// Kafka partition number
Property Partition As %Integer [ Required ];
 
/// Offset within the partition
Property KafkaOffset As %BigInt [ Required ];
 
/// Optional Kafka message key (used for partitioning on producer side)
Property MessageKey As %String(MAXLEN = 1000);
 
/// Message timestamp from Kafka headers (UTC)
Property KafkaTimestamp As %TimeStamp;
 
/// When the record was written to IRIS
Property CreatedAt As %TimeStamp [ SqlComputeCode = { Set {*} = $ZDATETIME($NOW(), 3) }, SqlComputed, SqlComputeOnChange = %%INSERT ];
 
/// Schema ID from Schema Registry — useful for tracing and debugging
/// when schemas evolve over time
Property SchemaId As %Integer;
 
/// Fully qualified protobuf message type (e.g. "com.example.Order")
Property ProtoType As %String(MAXLEN = 255);
 
/// Payload as JSON document. Use %DynamicObject API
/// to access nested fields without defining computed properties.
Property Payload As %DynamicObject;
 
/// Deduplication guard: at-least-once delivery from Kafka may produce
/// duplicate inserts on consumer restart. SQLCODE -119 on this index
/// is caught by the sink service and silently skipped.
Index UniqueOffset On (Topic, Partition, KafkaOffset) [ Unique ];
 
/// Supports typical analytical queries like
/// "all messages from topic X within time range"
Index TopicTime On (Topic, KafkaTimestamp);

ClassMethod GetByPath(json As %DynamicObject, path As %String) As %String [ CodeMode = expression ]
{
$XECUTE($$$FormatText("(json) Quit json.%1", path), json)
}
 
}